# im-prd-skill

[English](README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Español](README.es.md) | [Português](README.pt.md) | [Français](README.fr.md)

Um Claude Agent Skill para escrever PRDs de produtos de mensageria (IM) e sociais. Inclui uma biblioteca de 26 módulos sobre como os principais apps de mensagens tratam cada funcionalidade, para que as especificações geradas sigam por padrão as convenções de IM. Apenas os pontos em que os principais apps realmente divergem são levados a quem decide, como perguntas de múltipla escolha. Ele pode produzir somente um rascunho de entrega em Markdown ou também escrever os cartões de anotação em um canvas do Figma.

O skill foi criado para a equipe da ZYMIX. Esta edição pública remove as chaves de arquivo do Figma da equipe, os valores do sistema de design, as decisões internas e as evidências brutas; o fluxo de trabalho, a biblioteca de regras, os modelos, os scripts e os casos de avaliação estão intactos.

## Edições

| Edição | Caminho | Observações |
|---|---|---|
| English | [`en/box-prd-create/`](en/box-prd-create/) | Use esta para qualquer idioma que não seja o chinês. As regras estão em inglês; o rascunho de entrega é escrito no idioma do usuário. |
| 简体中文 | [`zh-CN/box-prd-create/`](zh-CN/box-prd-create/) | Edição original. Inclui os casos de avaliação (`evals/`) e o histórico completo de alterações. |

Ambas as edições usam o nome de skill `box-prd-create`; instale apenas uma delas.

## O que ele resolve

Pedir diretamente a uma IA que escreva a especificação de uma funcionalidade de IM costuma dar errado de três maneiras: regras incertas são escritas como se estivessem decididas; apenas o caminho feliz é coberto, deixando de fora estados como bloqueado, conta excluída, offline, multidispositivo e diferenças entre grupo e conversa individual; e as convenções do setor se misturam com as poucas decisões que a equipe realmente precisa tomar, de modo que quem decide tem de ler tudo para encontrá-las.

Como este skill lida com isso:

- **Biblioteca de regras em três níveis**: base (os principais apps concordam; seguir por padrão), convenção (a maioria dos apps faz assim; adotar a recomendação por padrão), divergência (os apps diferem; marcada como Must-ask (perguntar sempre) ou Default-OK (padrão aceitável)).
- **Só as perguntas obrigatórias são feitas**: no máximo 4 perguntas de múltipla escolha por rodada, com a opção recomendada primeiro. Todo o resto é escrito conforme a recomendação e listado linha a linha em "Defaulted to recommendation" (adotado conforme a recomendação) para revisão.
- **Matriz de cobertura de estados**: sucesso, falha, tempo esgotado, offline, permissões, sincronização multidispositivo e "a outra pessoa bloqueou você / excluiu a conta / saiu do grupo" são verificados um a um.
- **A incerteza permanece visível**: itens que precisam de decisão são escritos como `{TBD: topic, recommended: approach}` e fatos que faltam, como `{TBC: what is missing}`. Nada é apresentado como decidido.
- **Portão de escrita**: antes de mexer no Figma, o skill lista todos os nós que vai criar e os lotes; ele só escreve no canvas depois que quem decide aprova.

## Fluxo de trabalho

| Etapa | O que acontece |
|---|---|
| 0 Enquadramento do produto | Confirmar o tipo de conversa (individual / grupo / canal / comunidade), as plataformas, a criptografia de ponta a ponta, se desconhecidos podem alcançar os usuários e os pré-requisitos de viabilidade |
| 1 Fixar a fonte de verdade | Registrar o arquivo e os nós do Figma; marcar cada requisito como definido / a confirmar / sugerido |
| 2 Verificação das normas de IM | Ler os módulos correspondentes: seguir as bases, adotar as convenções por padrão e tratar as divergências conforme o nível |
| 3 Referência de concorrentes | Pesquisa externa apenas para capacidades que a biblioteca não cobre |
| 4 Matriz de cobertura de estados | Dimensões gerais mais os estados obrigatórios de cada módulo, cada um marcado como coberto / não aplicável / indefinido |
| 5 Rascunho primeiro | Escrever o rascunho de entrega em Markdown e executar `lint_card_text.py`; acrescentar um teste de leitura nos rascunhos maiores |
| 6 Layout e numeração | Planejar de uma só vez a ordem das telas, as linhas e a numeração |
| 7 Portão de escrita | `lint_card_text.py --gate` passa e quem decide aprova antes de qualquer escrita |
| 8 Escrever cartões e autoverificação | Autoverificação após cada lote; terminar com um recibo de aceitação |

Ordem do rascunho de entrega: Decisions for Box (decisões para o Box) → Defaulted to recommendation → Open items (pendências) → Role view summary (resumo por papel) → Cards (cartões) → Feature list (lista de funcionalidades) → Acceptance checkpoints (pontos de aceitação, ≤ 12) → Suggested follow-ups (próximos passos sugeridos).

## Estrutura

```
en/box-prd-create/              # Edição em inglês (mesma estrutura em zh-CN/)
├── SKILL.md                    # Fluxo de trabalho e roteamento (ponto de entrada)
├── references/
│   ├── im-norms/               # 26 módulos de IM + antipadrões + tabela de responsabilidades
│   ├── draft-template.md       # Modelo do rascunho de entrega e das notas de trabalho
│   ├── self-check.md           # Autoverificação da entrega
│   ├── canvas-layout.md        # Layout do canvas do Figma
│   ├── figjam.md               # Fluxogramas e lista de funcionalidades
│   ├── design-system.md        # Sistema de design (modelo, preencha o seu)
│   ├── rulings.md              # Decisões (modelo, preencha as suas)
│   └── HISTORY.md              # Histórico de alterações
└── scripts/
    ├── lint_card_text.py       # Lint do texto dos cartões (--gate para o portão de escrita)
    ├── lint_skill.py           # Autoverificação da estrutura da biblioteca de regras
    └── brand_terms.txt         # Nomes de marca proibidos
```

Módulos: contas e dispositivos, contatos e privacidade, lista de conversas, envio e confirmações, ações de mensagem, mídia e arquivos, grupos e canais, notificações, segurança e proteção, busca/chamadas/armazenamento, estrutura de páginas, padrões de interação, contas de serviço e bots, pagamentos no chat, feeds/canais/comunidades, mensagens avançadas, tradução e IA, descoberta/login/permissões, conta de carteira, convites e crescimento, idade e menores, sanções e recursos, publicidade e personalização, pontos e assinatura, central de privacidade, tickets de suporte.

## Instalação

Claude Code (edição em inglês como exemplo; use `zh-CN/box-prd-create` para chinês):

```bash
git clone https://github.com/ZBoxMan/im-prd-skill.git
```

```bash
cp -R im-prd-skill/en/box-prd-create ~/.claude/skills/
```

claude.ai: compacte a pasta `box-prd-create` em um zip e envie em Configurações → Recursos → Skills.

## Uso

Basta descrever a funcionalidade, por exemplo:

- "Adicione avisos de grupo aos chats em grupo. Escreva o PRD, por enquanto só o rascunho de entrega."
- "Adicione 'Baixar meus dados' em Configurações. Escreva o PRD no Figma: figma.com/design/<fileKey>, na zona de Configurações."
- "Quanto tempo deve durar o prazo para cancelar o envio de uma mensagem? Preciso disso no PRD."

## Adaptando para a sua equipe

- `references/design-system.md`: sua biblioteca de design, chaves de componentes e tokens de cor e tipografia (usado apenas ao desenhar telas de protótipo).
- `references/rulings.md`: as decisões de redação da sua equipe e os layouts descontinuados.
- `scripts/brand_terms.txt`: nomes de marca que não podem aparecer no texto dos cartões.
- "ZYMIX" e "Box" no SKILL.md são o nome do produto e quem decide; substitua conforme necessário.
- Escrever no Figma exige o Desktop Bridge do [figma-console MCP](https://github.com/southleft/figma-console-mcp). Rascunhos apenas em Markdown não precisam de nada adicional.
- `box-figma-prd` e `box-prd-review`, mencionados no SKILL.md, são skills complementares privados do autor (inspeção do canvas e revisão completa). O fluxo de geração funciona sem eles.

## Avaliação

Executada na edição em chinês:

- Comparação às cegas: 8 cenários (multidispositivo, administração de grupos, envelopes vermelhos, denúncias, enquetes de grupo, feed de amigos, integração de novos usuários, cancelar envio/editar) contra 21 skills semelhantes com o mesmo briefing. Um juiz Opus, sem saber a origem, pontuou correção em IM, cobertura de casos de borda, tratamento de decisões, viabilidade de implementação e legibilidade: 94 rodadas, 90 vitórias, 4 derrotas.
- Acionamento real: 31 prompts positivos e negativos × 3 execuções com `claude -p`: 31/31 corretos, sem falsos acionamentos nos negativos.

Registros: `zh-CN/box-prd-create/evals/trigger-results.md`. A edição em inglês não foi avaliada separadamente.

## Fontes e atualidade

Coletado em outubro de 2026 a partir do comportamento público dos principais clientes de mensagens, do código de clientes de código aberto, das centrais de ajuda oficiais e da documentação para desenvolvedores, e das especificações de protocolo. Os arquivos dos módulos não contêm nomes de marca; os detalhes por produto não são publicados. A maioria dos valores são padrões do cliente que os servidores podem substituir; revise a cada 90 dias.

## Licença

MIT
