"""Contrato do JSON de resultado entre a API e o front-end.

Define, com Pydantic, o formato exato das respostas de ``POST /analisar`` (sucesso e erro) e as
invariantes que todo resultado precisa cumprir. Também fixa a ordem das classes na saída do
modelo ONNX, compartilhada pelo treino (``handreplay_offline``) e pela API.

Camada mais baixa do pacote: só depende de pydantic e da biblioteca padrão.
Formato e versionamento: docs/adr/0003-contrato-json-versionado.md e a seção 7 do diagnóstico.
"""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

VERSAO_CONTRATO = "1.0.0"

NumeroPasso = Literal[1, 2, 3, 4, 5, 6]
Classe = Literal[1, 2, 3, 4, 5, 6, "outro", "incerto"]
StatusPasso = Literal["feito", "curto", "nao_detectado"]
StatusRegiao = Literal["coberto", "parcial", "nao_coberto"]
Faixa = Literal["MUITO BEM", "QUASE LÁ", "VAMOS DE NOVO"]
Orientacao = Literal["paisagem", "retrato"]
CodigoErro = Literal["arquivo_grande", "formato_invalido", "video_longo", "sem_lavagem"]

#: Ordem das colunas de probabilidade na saída do modelo: índice 0 é "outro", 1 a 6 são os passos.
CLASSES_MODELO: tuple[Literal["outro", 1, 2, 3, 4, 5, 6], ...] = ("outro", 1, 2, 3, 4, 5, 6)

#: Regiões do mapa das mãos, na ordem do JSON. O punho não pertence a nenhum passo e fica fora.
REGIOES = (
    "palmas",
    "dorso_maos",
    "espacos_dedos",
    "lado_palmar_dedos",
    "dorso_dedos",
    "polegares",
    "pontas_dedos",
)

#: Tempo mínimo somado para um passo contar como "feito" (Fase 3 do plano).
LIMIAR_FEITO_S = 2.0

#: HTTP de cada código de erro (seção 7.2 do diagnóstico): 2xx sempre traz resultado, 4xx traz erro.
STATUS_HTTP: dict[CodigoErro, int] = {
    "arquivo_grande": 413,
    "formato_invalido": 415,
    "video_longo": 422,
    "sem_lavagem": 422,
}

_TOLERANCIA_COBERTURA_S = 0.2  # um frame a 5 fps
_TOLERANCIA_CONTIGUIDADE_S = 1e-6
_TOLERANCIA_TEMPO_PASSO_S = 0.05


def faixa_da_nota(nota: int) -> Faixa:
    """Faixa exibida para a nota: 90 a 100, 60 a 89 e 0 a 59."""
    if nota >= 90:
        return "MUITO BEM"
    if nota >= 60:
        return "QUASE LÁ"
    return "VAMOS DE NOVO"


def status_do_tempo(tempo_s: float) -> StatusPasso:
    """Status de um passo pelo tempo somado: feito com 2 s ou mais, curto acima de 0 s."""
    if tempo_s >= LIMIAR_FEITO_S:
        return "feito"
    if tempo_s > 0:
        return "curto"
    return "nao_detectado"


class ErroAnalise(Exception):
    """Falha prevista da análise; vira uma ``RespostaErro`` com o HTTP de ``STATUS_HTTP``."""

    def __init__(self, codigo: CodigoErro, mensagem: str) -> None:
        super().__init__(mensagem)
        self.codigo: CodigoErro = codigo
        self.mensagem = mensagem


class _Modelo(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class Versao(_Modelo):
    contrato: str = Field(min_length=1)
    modelo: str = Field(min_length=1)
    regras: str = Field(min_length=1)


class FraseCard(_Modelo):
    texto: str = Field(min_length=1)
    destaque: str = Field(min_length=1)

    @model_validator(mode="after")
    def _destaque_faz_parte_do_texto(self) -> "FraseCard":
        if self.destaque not in self.texto:
            raise ValueError("frase_card.destaque precisa ser um trecho de frase_card.texto")
        return self


class Passo(_Modelo):
    numero: NumeroPasso
    nome: str = Field(min_length=1)
    nome_curto: str = Field(min_length=1)
    instrucao: str = Field(min_length=1)
    tempo_s: float = Field(ge=0)
    status: StatusPasso

    @model_validator(mode="after")
    def _status_coerente_com_tempo(self) -> "Passo":
        if self.status != status_do_tempo(self.tempo_s):
            raise ValueError(
                f"passo {self.numero}: status {self.status!r} não corresponde a {self.tempo_s} s"
            )
        return self


class Trecho(_Modelo):
    inicio_s: float = Field(ge=0)
    fim_s: float = Field(ge=0)
    classe: Classe
    confianca: float = Field(ge=0, le=1)

    @model_validator(mode="after")
    def _fim_depois_do_inicio(self) -> "Trecho":
        if self.fim_s <= self.inicio_s:
            raise ValueError("trecho com fim_s menor ou igual a inicio_s")
        return self


class Regioes(_Modelo):
    palmas: StatusRegiao
    dorso_maos: StatusRegiao
    espacos_dedos: StatusRegiao
    lado_palmar_dedos: StatusRegiao
    dorso_dedos: StatusRegiao
    polegares: StatusRegiao
    pontas_dedos: StatusRegiao


class PassoMaisLongo(_Modelo):
    numero: NumeroPasso
    tempo_s: float = Field(ge=0)


class Resumo(_Modelo):
    passos_completos: int = Field(ge=0, le=6)
    passo_mais_longo: PassoMaisLongo


class Resultado(_Modelo):
    """Resposta de sucesso de ``POST /analisar`` (HTTP 200)."""

    versao: Versao
    duracao_s: float = Field(ge=0)
    orientacao: Orientacao
    nota: int = Field(ge=0, le=100)
    faixa: Faixa
    frase_tela: str = Field(min_length=1)
    frase_card: FraseCard
    passos: list[Passo] = Field(min_length=6, max_length=6)
    trechos: list[Trecho] = Field(min_length=1)
    regioes: Regioes
    resumo: Resumo

    @model_validator(mode="after")
    def _invariantes(self) -> "Resultado":
        if [p.numero for p in self.passos] != [1, 2, 3, 4, 5, 6]:
            raise ValueError("passos precisam vir numerados de 1 a 6, em ordem")
        if self.faixa != faixa_da_nota(self.nota):
            raise ValueError(f"faixa {self.faixa!r} não corresponde à nota {self.nota}")
        self._conferir_trechos()
        self._conferir_tempos_dos_passos()
        self._conferir_resumo()
        return self

    def _conferir_trechos(self) -> None:
        if abs(self.trechos[0].inicio_s) > _TOLERANCIA_COBERTURA_S:
            raise ValueError("o primeiro trecho precisa começar em 0 s")
        for anterior, seguinte in zip(self.trechos, self.trechos[1:], strict=False):
            if abs(seguinte.inicio_s - anterior.fim_s) > _TOLERANCIA_CONTIGUIDADE_S:
                raise ValueError(f"trechos não contíguos em {anterior.fim_s} s")
        if abs(self.trechos[-1].fim_s - self.duracao_s) > _TOLERANCIA_COBERTURA_S:
            raise ValueError("o último trecho precisa terminar em duracao_s")

    def _conferir_tempos_dos_passos(self) -> None:
        for passo in self.passos:
            soma = sum(t.fim_s - t.inicio_s for t in self.trechos if t.classe == passo.numero)
            if abs(soma - passo.tempo_s) > _TOLERANCIA_TEMPO_PASSO_S:
                raise ValueError(
                    f"passo {passo.numero}: tempo_s {passo.tempo_s} difere da soma dos trechos"
                    f" ({soma:.2f} s)"
                )

    def _conferir_resumo(self) -> None:
        feitos = sum(p.status == "feito" for p in self.passos)
        if self.resumo.passos_completos != feitos:
            raise ValueError("resumo.passos_completos difere do número de passos feitos")
        maior = self.resumo.passo_mais_longo
        tempo_maximo = max(p.tempo_s for p in self.passos)
        if self.passos[maior.numero - 1].tempo_s != maior.tempo_s or maior.tempo_s != tempo_maximo:
            raise ValueError("resumo.passo_mais_longo não é o passo de maior tempo")


class Erro(_Modelo):
    codigo: CodigoErro
    mensagem: str = Field(min_length=1)


class RespostaErro(_Modelo):
    """Resposta de erro de ``POST /analisar`` (HTTP 4xx, conforme ``STATUS_HTTP``)."""

    versao: Versao
    erro: Erro
