# Inteligência de Estoque: Otimização de Compras e Prevenção de Ruptura

> 📱 **Nota de Desenvolvimento:** Este projeto foi totalmente planejado, estruturado e testado em ambiente mobile utilizando o smartphone (IDE Pydroid 3), demonstrando adaptabilidade e foco em entrega sob qualquer cenário.

## 📌 O Cenário de Negócio
No dia a dia de uma operação de varejo ou indústria, o maior desafio de um **Analista de Planejamento de Compras** é equilibrar dois pratos:
1. **Nunca deixar o produto faltar** na prateleira (Ruptura), o que significa perda de vendas e clientes insatisfeitos.
2. **Nunca comprar produto demais**, o que significa dinheiro da empresa congelado no estoque que poderia estar sendo usado em outra área.

Este projeto resolve essa dor combinando dados físicos de inventário com o fluxo histórico de pedidos para automatizar e direcionar as decisões de abastecimento de forma inteligente.

## 🧠 Como a Inteligência foi Construída (A Lógica do Projeto)

O projeto processa os dados em duas etapas estratégicas para garantir que o gerente da área saiba exatamente onde agir:

### Etapa 1: Classificação de Relevância Financeira (Curva ABC)
Nem todo produto tem o mesmo peso no caixa da empresa. O algoritmo ordena o estoque do item mais valioso para o mais barato e calcula o impacto acumulado no orçamento:
* **Classe A (Críticos):** Concentram a maior parte do capital da empresa (até 80%). Uma falha aqui é catastrófica. O sistema garante atenção total a eles.
* **Classe B (Intermediários):** Produtos de impacto médio (próximos 15%).
* **Classe C (Rotineiros):** Produtos baratos e de baixo impacto (os 5% finais).

### Etapa 2: Motor Dinâmico de Alertas de Compra
Em vez de usar uma regra fixa de dias para comprar produtos, o sistema calcula uma **velocidade de escoamento individual** para cada SKU. 
* O algoritmo descobre exatamente em quantos dias o estoque atual vai zerar se a demanda continuar constante.
* Em seguida, o sistema cruza esse tempo com o **Lead Time (prazo de entrega)** do fornecedor daquele produto específico.
* Se o estoque for durar menos tempo do que o fornecedor leva para entregar o caminhão no pior cenário, o sistema dispara um aviso automático de **`CRÍTICO: Risco de Ruptura`**. Se o tempo for menor que a média de entrega, o status muda para **`ALERTA`**.

## 📊 Relatórios de Apoio à Decisão (Camada de Dados)
Com a base tratada e inteligente, a solução espelha os dados em uma estrutura relacional para extrair respostas rápidas que o gerente da área precisa para a tomada de decisão diária:
1. **Mapeamento de Urgências:** Lista imediata dos produtos Classe A (mais caros) que estão em estado crítico de falta.
2. **Balanço Financeiro:** Soma exata do capital imobilizado por categoria para prestação de contas com a diretoria financeira.
3. **Auditoria de Fornecedores:** Identificação de quais parceiros comerciais concentram os maiores riscos de desabastecimento da cadeia.

## 🚀 Resultados Práticos do Modelo (Console)

O cruzamento de dados gerou insights automáticos e imediatos para a tomada de decisão do Diretor de Compras:

### 1. Monitoramento Dinâmico de Alertas e Prazos de Entrega (Lead Time)
O motor do projeto identificou exatamente quais produtos vão faltar antes do caminhão do fornecedor chegar, sem engessar nenhuma regra de dias:

*   **SKU 1193BA (CRÍTICO):** Tem apenas **4.1 dias** de estoque e o fornecedor leva até **138 dias** para entregar. Compra urgente!
*   **SKU 1964BA (CRÍTICO):** Tem apenas **7.1 dias** de estoque e o fornecedor demora até **96 dias** para entregar.
*   **SKU 2449CA (Saudável):** Tem estoque seguro para **2.309 dias**, muito acima dos 68 dias do fornecedor. Não precisa gastar dinheiro comprando agora.

### 2. Resumo Gerencial de Capital Preso (Curva ABC)
Provamos financeiramente que a empresa tem **R$ 43 milhões** travados em apenas **64 produtos** estratégicos, o que justifica o foco total do analista nesses itens (Classe A).

| Classe | Total de Itens | Capital Total Investido | Estratégia de Ação |
| :--- | :---: | :---: | :--- |
| **Classe A** | 64 | R$ 43.193.694,08 | Monitoramento diário e auditoria |
| **Classe B** | 67 | R$ 8.167.913,75 | Revisão quinzenal de estoque |
| **Classe C** | 172 | R$ 2.768.870,52 | Compras automáticas em lote |

### 3. Gestão e Auditoria de Fornecedores Ofensores
O relatório mapeou via SQL quais parceiros comerciais concentram as maiores falhas e riscos de desabastecimento na nossa operação hoje:

1. **Lake Ltd:** lidera o risco com **43 produtos** em estado crítico.
2. **ALK-Abello, Corp:** **28 produtos** em estado crítico.
3. **Cixi Group:** **27 produtos** em estado crítico.

# supply-chain-analytics
