# 001 - Utilização do Gemini via AI-as-a-Service

**Status:** Aceito

## Contexto
O projeto ADR Maker precisa transformar anotações informais de desenvolvedores em arquivos estruturados em Markdown utilizando Processamento de Linguagem Natural avançado. Para cumprir essa funcionalidade de GenAI, é necessário decidir como o modelo de linguagem (LLM) será disponibilizado, executado e consumido pela aplicação. O escopo do projeto é pequeno, não há infraestrutura pesada provisionada, e espera-se que a solução seja barata, de baixa latência e de integração direta.

## Problema
Como integrar a inteligência artificial generativa de forma que atenda às demandas de latência de uma aplicação web síncrona sem incorrer em alta complexidade de infraestrutura ou custos inviáveis de manutenção?

## Decisão
Decidimos adotar uma arquitetura de **AI-as-a-Service** consumindo a API do modelo proprietário hospedado em nuvem pelo Google (Gemini 3.6 Flash), integrando-o ao backend da nossa aplicação via o SDK oficial `google-genai`.

## Consequências positivas
- **Zero Complexidade de Infraestrutura:** A aplicação backend lida apenas com tráfego HTTP. O provisionamento e manutenção pesada de GPUs ficam por conta do provedor (Google).
- **Baixa Latência:** Ao usar o modelo da classe "Flash", a aplicação consegue respostas extremamente rápidas, mantendo a responsividade do fluxo síncrono no browser sem necessidade de sistemas de webhooks complexos.
- **Custo Inicial Quase Nulo:** Modelos gerenciados costumam oferecer limites gratuitos generosos (Free Tier) ou tarifação *pay-as-you-go* na fração de centavo. Como a aplicação não possui uso contínuo assíncrono nem dados em massa, os custos beiram zero.

## Consequências negativas
- **Dependência (Vendor Lock-in):** Ficamos atrelados aos formatos de API e disponibilidade do Google. Se a API deles cair, a geração de ADR fica 100% inoperante.
- **Privacidade Reduzida:** Decisões arquiteturais de infraestrutura da empresa usuária da ferramenta precisarão ser transitadas pela internet pública para os servidores do provedor da API de IA, o que pode esbarrar em políticas restritas de *compliance* ou segurança de dados em algumas companhias.

## Alternativas Consideradas

### 1. AI-as-a-Service usando Gemini API (Alternativa Escolhida)
- **Custo:** Extramente baixo, cobrado apenas por tokens consumidos sob demanda.
- **Latência:** Baixa, otimizada para respostas rápidas (modelo Flash).
- **Complexidade Operacional:** Baixíssima. Requer apenas o gerenciamento de uma API Key.
- **Controle sobre o modelo:** Baixo. Sem capacidade de re-treinamento ou ajustes profundos dos pesos do modelo.
- **Privacidade:** Moderada a baixa, visto que o dado deve deixar o perímetro da aplicação para ir à rede do provedor.
- **Necessidade de Infraestrutura:** Mínima (servidor web simples consegue operar a integração).

### 2. Modelo Open-Weight executado localmente (ex: Llama 3 via Ollama)
- **Custo:** Alto custo fixo em *compute* de hardware.
- **Latência:** Alta ou variável, a depender inteiramente da potência da máquina onde o backend estiver rodando.
- **Complexidade Operacional:** Alta. Obriga o provisionamento, monitoramento de saúde do modelo, escalonamento e gestão de dependências pesadas de hardware (CUDA, drivers).
- **Controle sobre o modelo:** Muito Alto. Pode ser customizado com Fine-tuning profundo.
- **Privacidade:** Total. O dado sensível sobre as decisões da arquitetura não sai do perímetro corporativo.
- **Necessidade de Infraestrutura:** Altíssima (servidores on-premise com GPUs robustas ou instâncias EC2 otimizadas extremamente caras, o que mataria o conceito de escopo pequeno definido para o ADR Maker).

### 3. AI Gateway (ex: Kong AI Gateway ou Cloudflare AI)
- **Custo:** Moderado. Pode encarecer devido à necessidade de manter a licença/servidor do Gateway além do uso de API da LLM.
- **Latência:** Média. Insere um pequeno salto adicional (*hop*) na rede para processar métricas de gateway.
- **Complexidade Operacional:** Média. Adiciona um componente autônomo extra na arquitetura apenas para intermediar as chamadas.
- **Controle sobre o modelo:** Moderado (provê abstração, mas depende dos conectores que o Gateway suporta).
- **Privacidade:** Depende do destino final configurado pelo Gateway, mas no mínimo embute a preocupação em gerir o log centralizado do Gateway que passa a deter tudo o que for processado.
- **Necessidade de Infraestrutura:** Média. 
- **Por que não foi escolhida:** Dado que este projeto provê um único endpoint síncrono para o próprio modelo e não há exigência atual de balanceamento de carga, rate-limit severo ou rodízio de modelos, adicionar um AI Gateway representaria uma engenharia excessiva (*overengineering*) violando o requisito de simplicidade e baixo custo inicial.
