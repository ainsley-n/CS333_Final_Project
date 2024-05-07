
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.matches = []

    def draw(self, cards):
        self.hand.extend(cards)

    def ask(self, other_player, rank):
        matching_cards = [card for card in other_player.hand if card.rank == rank]
        if matching_cards:
            other_player.hand = [card for card in other_player.hand if card.rank != rank]
            self.hand.extend(matching_cards)
            return True
        else:
            return False

    def check_for_matches(self):
        ranks_count = {}
        for card in self.hand:
            if card.rank in ranks_count:
                ranks_count[card.rank] += 1
            else:
                ranks_count[card.rank] = 1

        # print("Ranks count:", ranks_count)

        for rank, count in ranks_count.items():
            if count == 4:
                self.matches.append(rank)
                self.hand = [card for card in self.hand if card.rank != rank]

        # print("Matches:", self.matches)

        # print("Updated hand after removing matches:", self.hand)

        return len(self.matches)

