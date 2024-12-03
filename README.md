# **Chatbot de Futebol – Documentação**

Este é um chatbot interativo de futebol que permite aos usuários consultar resultados de jogos, próximos confrontos, classificação, estatísticas de jogadores, além de adicionar novos jogos à base de dados. O chatbot utiliza técnicas de Processamento de Linguagem Natural (NLP) para interpretar comandos de texto e oferece uma interface no terminal para interação.

---

## **Funcionalidades**

1. **Consultar Resultados Recentes**: Exibe os resultados dos jogos finalizados.
2. **Listar Próximos Jogos**: Mostra as próximas partidas agendadas.
3. **Exibir Classificação**: Fornece uma tabela de classificação fictícia.
4. **Mostrar Estatísticas**: Apresenta as estatísticas de jogadores e times.
5. **Adicionar Novo Jogo**: Permite adicionar uma nova partida ao calendário.
6. **Interface Interativa**: O usuário interage com o chatbot via terminal.

---

## **Técnicas Utilizadas**

- **Processamento de Linguagem Natural (NLP)**:
  - Tokenização com `nltk.tokenize.word_tokenize`.
  - Remoção de stop words usando `nltk.corpus.stopwords`.
  - Stemização com `nltk.stem.RSLPStemmer` para identificar a raiz das palavras.
- **Fuzzy Matching**: Utilização da biblioteca `fuzzywuzzy` para encontrar correspondências aproximadas entre palavras e intenções do usuário.
- **Estrutura em Árvore**: Navegação de intenções e entidades através de uma estrutura de árvore personalizada.

---

## **Tecnologias Necessárias**

Antes de rodar o projeto, certifique-se de ter as seguintes tecnologias instaladas:

- **Python 3.8+**
- **Bibliotecas Python**:
  - `nltk`
  - `pandas`
  - `fuzzywuzzy`
  - `python-Levenshtein` (para melhorar o desempenho do `fuzzywuzzy`)

---

## **Instruções de Uso**

### 1. **Clonar o Repositório**

```bash
git clone <URL_DO_REPOSITORIO>
cd <NOME_DO_REPOSITORIO>
```

---

### 2. **Criar o Ambiente Virtual**

#### No Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

#### No macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. **Instalar as Dependências**

Com o ambiente virtual ativado, instale as dependências necessárias:

```bash
pip install -r requirements.txt
```

> **Nota:** Caso não tenha um arquivo `requirements.txt`, você pode criar um manualmente com o seguinte conteúdo:

```
nltk
pandas
fuzzywuzzy
python-Levenshtein
```

---

### 4. **Baixar Recursos do NLTK**

Execute o seguinte código em um terminal Python para baixar os pacotes necessários do `nltk`:

```python
import nltk
nltk.download('punkt')
nltk.download('rslp')
nltk.download('stopwords')
```

---

### 5. **Executar o Chatbot**

Execute o chatbot com o seguinte comando:

```bash
python main.py
```

> **Nota:** Substitua `main.py` pelo nome correto do arquivo Python que contém o chatbot.

---

## **Como Utilizar o Chatbot**

Após iniciar o chatbot, você será recebido com uma saudação no terminal e poderá interagir com ele fornecendo comandos como:

- **"Resultados"**: Exibe os últimos resultados.
- **"Próximos Jogos"**: Lista as próximas partidas.
- **"Classificação"**: Mostra a classificação atual (exemplo fictício).
- **"Estatísticas"**: Exibe estatísticas de jogadores.
- **"Adicionar Jogo"**: Permite adicionar uma nova partida ao calendário.
- **"Sair"**: Encerra a execução do chatbot.

---

## **Exemplo de Uso**

### 1. **Consultar Resultados**

Entrada no terminal:

```
O que você gostaria de fazer? (Resultados | Próximos Jogos | Classificação | Estatísticas | Adicionar Jogo | Sair): gostaria de saber os resultados dos jogos, por favor
```

Saída esperada:

```
Resultados Recentes:
Flamengo 3 x 1 Corinthians - 01/12/2023
Palmeiras 1 x 1 São Paulo - 02/12/2023
Grêmio 0 x 2 Internacional - 03/12/2023
```

---

# **Chatbot de Futebol – Documentação Completa**

Este chatbot de futebol permite que o usuário interaja via terminal para obter informações sobre resultados, próximos jogos, classificação, estatísticas e ainda adicionar novas partidas ao calendário de jogos. Ele utiliza técnicas de **Processamento de Linguagem Natural (NLP)** para interpretar os comandos do usuário e uma estrutura em árvore para navegar pelas intenções.

---

## **Funcionalidades**

1. **Consultar Resultados Recentes**: Exibe os resultados dos jogos finalizados.
2. **Listar Próximos Jogos**: Mostra as próximas partidas agendadas.
3. **Exibir Classificação**: Fornece uma tabela de classificação fictícia.
4. **Mostrar Estatísticas**: Apresenta as estatísticas de jogadores e times.
5. **Adicionar Novo Jogo**: Permite adicionar uma nova partida ao calendário.
6. **Interface Interativa**: O usuário interage com o chatbot via terminal.

---

## **Explicação do Funcionamento do Chatbot**

O chatbot possui uma estrutura baseada em **Intenção e Entidade**, onde:

- **Intenção**: Representa a ação que o usuário deseja realizar (ex: consultar resultados, listar próximos jogos).
- **Entidade**: Refere-se ao contexto ou assunto relacionado à intenção (ex: "jogo").

A interação funciona da seguinte forma:

1. O usuário fornece um comando no terminal.
2. O chatbot processa a entrada, tokeniza o texto e identifica as intenções e entidades.
3. Com base na intenção identificada, a função correspondente é executada.
4. O chatbot responde com a informação solicitada.

---

## **Arquitetura do Código**

### 1. **Classe `Node`**

A classe `Node` representa um nó na árvore de intenções.

```python
@dataclass
class Node:
    value: str
    synonyms: List[str] = field(default_factory=list)
    children: List['Node'] = field(default_factory=list)
```

- **`value`**: Nome da intenção ou entidade.
- **`synonyms`**: Lista de sinônimos que ajudam na correspondência com o valor.
- **`children`**: Lista de nós filhos, representando subintenções ou subentidades.

---

### 2. **Classe `Tree`**

A classe `Tree` gerencia a estrutura em árvore que mapeia intenções e entidades.

```python
class Tree:
    def __init__(self, root_value: str):
        self.root = Node(root_value)
```

#### Principais Funções:

- **`add_child`**: Adiciona uma intenção filha a uma entidade pai.
- **`search`**: Busca por um nó na árvore com base em um valor ou sinônimo, utilizando fuzzy matching.

---

### 3. **Classe `FootballChatBot`**

A classe principal do chatbot que gerencia a interação com o usuário.

```python
class FootballChatBot:
    def __init__(self):
        self.tree = self._build_intent_tree()
        self.intent_function_map = self._get_intent_function_map()
        self.stemmer = RSLPStemmer()
        self.stop_words = set(stopwords.words('portuguese'))
        self.games_df = pd.DataFrame({...})
```

#### Atributos:

- **`tree`**: A árvore de intenções e entidades.
- **`intent_function_map`**: Um dicionário que mapeia intenções para funções.
- **`stemmer`**: Responsável por converter palavras para suas raízes (stemming).
- **`stop_words`**: Conjunto de palavras irrelevantes que são ignoradas na tokenização.
- **`games_df`**: DataFrame que armazena os jogos, resultados e próximos confrontos.

---

### **Funções Principais do Chatbot**

#### 1. **`_build_intent_tree`**

Constrói a árvore de intenções.

```python
def _build_intent_tree(self) -> Tree:
    intent_tree = Tree("chatbot")
    intent_tree.add_child("chatbot", "jogo")
    intent_tree.add_child("jogo", "result", synonyms=["placar", "resultado", "gols", "score", "últimos jogos"])
    intent_tree.add_child("jogo", "proxim", synonyms=["futuro", "agenda", "próximos"])
    intent_tree.add_child("jogo", "classific", synonyms=["tabela", "ranking", "posição"])
    intent_tree.add_child("jogo", "estat", synonyms=["estatísticas", "números", "desempenho"])
    intent_tree.add_child("jogo", "adicion", synonyms=["incluir", "novo jogo", "adicionar"])
    return intent_tree
```

---

#### 2. **`process_prompt`**

Processa o comando do usuário, identifica a intenção e executa a ação correspondente.

```python
def process_prompt(self, prompt: str):
    tokens = self._tokenize_and_clean(prompt)
    entity = self._find_entity(tokens)
    intent = self._find_intent(tokens, entity)

    if intent:
        self._execute_intent(intent)
    else:
        print("Desculpe, não entendi sua solicitação.")
```

---

#### 3. **`_tokenize_and_clean`**

Tokeniza e limpa o comando do usuário, removendo stop words e pontuações.

```python
def _tokenize_and_clean(self, prompt: str) -> List[str]:
    return [
        self.stemmer.stem(token) for token in word_tokenize(prompt.lower())
        if token not in self.stop_words and token not in string.punctuation
    ]
```

---

#### 4. **`_find_entity`**

Busca por uma entidade dentro dos tokens fornecidos.

```python
def _find_entity(self, tokens: List[str]) -> Optional[Node]:
    for token in tokens:
        entity = self.tree.search(token)
        if entity:
            return entity
    return None
```

---

#### 5. **`_find_intent`**

Busca por uma intenção associada à entidade.

```python
def _find_intent(self, tokens: List[str], entity: Optional[Node]) -> Optional[Node]:
    if entity:
        for token in tokens:
            intent = self.tree.search(token, entity)
            if intent:
                return intent
    return None
```

---

#### 6. **`_execute_intent`**

Executa a função associada à intenção identificada.

```python
def _execute_intent(self, intent: Node):
    action = self.intent_function_map.get(intent.value)
    if action:
        action()
```

---

#### Funções de Ação

1. **`list_results`**: Lista os resultados dos jogos finalizados.
2. **`list_next_games`**: Lista os próximos jogos agendados.
3. **`show_standings`**: Mostra a tabela de classificação.
4. **`show_statistics`**: Exibe as estatísticas dos jogadores.
5. **`add_next_game`**: Permite adicionar uma nova partida ao calendário.

---

## **Possíveis Problemas e Soluções**

1. **Problema**: `ModuleNotFoundError: No module named 'nltk'`
   - **Solução**: Certifique-se de que o ambiente virtual está ativado e instale as dependências com `pip install nltk`.

2. **Problema**: `PermissionError: [Errno 13] Permission denied` ao ativar o ambiente virtual.
   - **Solução**: Conceda permissão de execução ao arquivo de ativação do ambiente virtual:
     ```bash
     chmod +x venv/bin/activate  # Para macOS/Linux
     ```

3. **Problema**: Comando não reconhecido pelo chatbot.
   - **Solução**: Certifique-se de que está utilizando palavras relacionadas às intenções definidas no código.

---