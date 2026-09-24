"""Todos os textos que a API devolve: nomes, instruções, regiões, frases e mensagens de erro.

Esqueleto, implementado na Fase 3; o texto final é revisado na semana 8.

Separado de ``regras`` para que revisar texto não exija mexer em lógica testada. As tabelas vêm
das Fases 3, 5 e 6 do plano (nome, nome curto, instrução, regiões que cada passo acende, frases
"Faltou ...", "... ficou curto" e as frases do card com o trecho em destaque).

Dependências permitidas: ``handreplay.contrato``.
"""

from dataclasses import dataclass

from handreplay.contrato import CodigoErro, NumeroPasso


@dataclass(frozen=True)
class TextosPasso:
    nome: str
    nome_curto: str
    instrucao: str
    regioes: tuple[str, ...]
    #: Fragmento usado em "Faltou ..." e "... ficou curto" na frase da tela.
    fragmento_tela: str
    frase_card_nao_detectado: str
    frase_card_curto: str
    #: Parte da frase do card que aparece em coral.
    destaque_card: str


def textos_do_passo(numero: NumeroPasso) -> TextosPasso:
    """Textos de um dos 6 passos da OMS."""
    raise NotImplementedError("Fase 3")


def mensagem_de_erro(codigo: CodigoErro) -> str:
    """Mensagem legível para cada código de erro do contrato."""
    raise NotImplementedError("Fase 3")
