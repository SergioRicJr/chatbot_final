import nltk
import pandas as pd
import string
from dataclasses import dataclass, field
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer
from typing import List, Dict, Optional, Callable
from fuzzywuzzy import fuzz

nltk.download('punkt')
nltk.download('rslp')
nltk.download('stopwords')

@dataclass
class Node:
    value: str
    synonyms: List[str] = field(default_factory=list)
    children: List['Node'] = field(default_factory=list)

class Tree:
    def __init__(self, root_value: str):
        self.root = Node(root_value)

    def add_child(self, parent_value: str, child_value: str, synonyms: List[str] = None):
        parent_node = self.search(parent_value)
        if parent_node and not any(child.value == child_value for child in parent_node.children):
            parent_node.children.append(Node(child_value, synonyms or []))

    def search(self, value: str, node: Optional[Node] = None) -> Optional[Node]:
        node = node or self.root
        if fuzz.ratio(node.value, value) > 80 or any(fuzz.ratio(syn, value) > 80 for syn in node.synonyms):
            return node
        for child in node.children:
            result = self.search(value, child)
            if result:
                return result
        return None

class FootballChatBot:
    def __init__(self):
        self.tree = self._build_intent_tree()
        self.intent_function_map = self._get_intent_function_map()
        self.stemmer = RSLPStemmer()
        self.stop_words = set(stopwords.words('portuguese'))
        self.games_df = pd.DataFrame({
            'game_id': [1, 2, 3],
            'home_team': ['Flamengo', 'Palmeiras', 'Grêmio'],
            'away_team': ['Corinthians', 'São Paulo', 'Internacional'],
            'home_score': [3, 1, 0],
            'away_score': [1, 1, 2],
            'date': pd.to_datetime(['2023-12-01', '2023-12-02', '2023-12-03'])
        })

    def _build_intent_tree(self) -> Tree:
        intent_tree = Tree("chatbot")
        intent_tree.add_child("chatbot", "jogo")
        intent_tree.add_child("jogo", "result", synonyms=[
            "placar", "resultado", "resultados", "jogos anteriores", "finalizado", "terminado", "pontuação", 
            "gols", "score", "últimos jogos", "jogos passados", "histórico", "balanço", "performance", 
            "marcadores", "informação de jogo", "resumo", "destaques", "última partida"
        ])

        intent_tree.add_child("jogo", "proxim", synonyms=[
            "futuro", "agenda", "próximos", "partidas futuras", "jogos seguintes", "programação", "agendado", 
            "calendário", "em breve", "próxima rodada", "próximos confrontos", "partidas agendadas", 
            "jogos futuros", "próximas partidas", "planejado", "agenda esportiva", "confrontos futuros", "eventos futuros"
        ])

        intent_tree.add_child("jogo", "classific", synonyms=[
            "tabela", "ranking", "posição", "classificação", "ordem", "pontuação geral", "liderança", 
            "ranking geral", "colocação", "situação", "topo da tabela", "pontos acumulados", "posição na tabela", 
            "posição atual", "tabela geral", "classificação atual", "posição dos times", "liderança atual", "ranking esportivo"
        ])

        intent_tree.add_child("jogo", "estat", synonyms=[
            "estatísticas", "números", "desempenho", "dados", "informações", "média", "jogadores em destaque", 
            "principais marcadores", "estatísticas de jogo", "análise", "detalhes", "informações de desempenho", 
            "destaques individuais", "dados esportivos", "estatísticas detalhadas", "métricas", "principais jogadores", 
            "ranking de desempenho", "estatísticas de temporada"
        ])

        intent_tree.add_child("jogo", "adicion", synonyms=[
            "incluir", "cadastrar", "novo jogo", "adicionar", "inserir", "registrar", "agendar", "marcar", 
            "incluir nova partida", "programar", "novo evento", "adicionar jogo", "criar novo jogo", "adicionar à agenda", 
            "agendar confronto", "cadastrar partida", "registrar jogo", "marcar evento"
        ])
        return intent_tree

    def _get_intent_function_map(self) -> Dict[str, Callable]:
        return {
            'result': self.list_results,
            'proxim': self.list_next_games,
            'classific': self.show_standings,
            'estat': self.show_statistics,
            'adicion': self.add_next_game
        }

    def process_prompt(self, prompt: str):
        tokens = self._tokenize_and_clean(prompt)
        entity = self._find_entity(tokens)
        intent = self._find_intent(tokens, entity)

        if intent:
            self._execute_intent(intent)
        else:
            print("Desculpe, não entendi sua solicitação.")

    def _tokenize_and_clean(self, prompt: str) -> List[str]:
        return [
            self.stemmer.stem(token) for token in word_tokenize(prompt.lower()) 
            if token not in self.stop_words and token not in string.punctuation
        ]

    def _find_entity(self, tokens: List[str]) -> Optional[Node]:
        for token in tokens:
            entity = self.tree.search(token)
            if entity:
                return entity
        return None

    def _find_intent(self, tokens: List[str], entity: Optional[Node]) -> Optional[Node]:
        if entity:
            for token in tokens:
                intent = self.tree.search(token, entity)
                if intent:
                    return intent
        return None

    def _execute_intent(self, intent: Node):
        action = self.intent_function_map.get(intent.value)
        if action:
            action()

    def list_results(self):
        print("\nResultados Recentes:")
        for _, row in self.games_df.iterrows():
            if row['date'] <= pd.Timestamp.now():
                print(f"{row['home_team']} {row['home_score']} x {row['away_score']} {row['away_team']} - {row['date'].strftime('%d/%m/%Y')}")

    def list_next_games(self):
        upcoming_games = self.games_df[self.games_df['date'] > pd.Timestamp.now()]
        if not upcoming_games.empty:
            print("\nPróximos Jogos:")
            for _, row in upcoming_games.iterrows():
                print(f"{row['home_team']} x {row['away_team']} - {row['date'].strftime('%d/%m/%Y')}")
        else:
            print("\nNão há próximos jogos agendados.")

    def show_standings(self):
        print("\nTabela de Classificação (Exemplo Fictício)")
        print("Flamengo: 45 pontos")
        print("Palmeiras: 43 pontos")
        print("Grêmio: 40 pontos")

    def show_statistics(self):
        print("\nEstatísticas de Jogadores:")
        print("Gabriel Barbosa (Flamengo): 12 gols")
        print("Rony (Palmeiras): 10 gols")
        print("Luís Suárez (Grêmio): 8 gols")

    def add_next_game(self):
        try:
            home_team = input("Digite o nome do time da casa: ").strip()
            away_team = input("Digite o nome do time visitante: ").strip()
            date_str = input("Digite a data do jogo (YYYY-MM-DD): ").strip()
            date = pd.to_datetime(date_str, format='%Y-%m-%d', errors='coerce')

            if pd.isna(date):
                print("Data inválida. Por favor, use o formato correto.")
                return

            new_game = {
                'game_id': self.games_df['game_id'].max() + 1 if not self.games_df.empty else 1,
                'home_team': home_team,
                'away_team': away_team,
                'home_score': None,
                'away_score': None,
                'date': date
            }
            self.games_df = pd.concat([self.games_df, pd.DataFrame([new_game])], ignore_index=True)
            print(f"Jogo {home_team} x {away_team} adicionado com sucesso para a data {date.strftime('%d/%m/%Y')}!")
            self.list_next_games()
        except Exception as e:
            print(f"Erro ao adicionar o jogo: {e}")

    def run(self):
        print("Olá, seja bem-vindo(a) ao chatbot de futebol!")
        while True:
            prompt = input("\nO que você gostaria de fazer? (Resultados | Próximos Jogos | Classificação | Estatísticas | Adicionar Jogo | Sair): ").lower()
            if prompt == 'sair':
                print("Até mais!")
                break
            self.process_prompt(prompt)

if __name__ == "__main__":
    bot = FootballChatBot()
    bot.run()
