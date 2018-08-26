import game

def play(hand, is_start_of_round, play_to_beat, round_history, player_no, hand_sizes, scores, round_no):
  isStart = is_start_of_round
  trick = play_to_beat
  history = round_history
  me = player_no
  handSizes = hand_sizes
  round = round_no
  """
  The parameters to this function are:
  * `hand`: A list of card strings that are the card(s) in your hand.
  * `is_start_of_round`: A Boolean that indicates whether or not the `play` function is being asked to make the first play of a round.
  * `play_to_beat`: The current best play of the trick. If no such play exists (you are the first play in the trick), this will be an empty list.
  * `round_history`: A list of *trick_history* entries.
    A *trick_history* entry is a list of *trick_play* entries.
    Each *trick_play* entry is a `(player_no, play)` 2-tuple, where `player_no` is an integer between 0 and 3 (inclusive) indicating which player made the play, and `play` is the play that said player made, which will be a list of card strings.
  * `player_no`: An integer between 0 and 3 (inclusive) indicating which player number you are in the game.
  * `hand_sizes`: A 4-tuple of integers representing the number of cards each player has in their hand, in player number order.
  * `scores`: A 4-tuple of integers representing the score of each player at the start of this round, in player number order.
  * `round_no`: An integer between 0 and 9 (inclusive) indicating which round number is currently being played.

  This function should return an empty list (`[]`) to indicate a pass (see "Playing a Round"), or a list of card strings, indicating that you want to play these cards to the table as a valid play.
  """
  # hand, isStart, trick, history, me, handSizes, scores, round

  # http://jsfiddle.net/9zu1nx0t/6/

  hand = game.toCards(hand)
  melds = sorted(game.findMelds(hand))

  if isStart:
    melds = game.filterMelds(lambda meld: game.Card("3D") in meld, melds)

  if len(trick) == 0:
    return melds[-1].strings()

  trick = game.Meld(trick)
  legal = sorted(game.filterLegal(melds, trick))

  # legal = game.filterMelds(lambda meld: meld.breaking(melds) == 0, legal)
  legal.sort(key=lambda meld: (len(meld.breaking(melds)), meld))

  if len(legal) == 0: return []
  return legal[0].strings()

if __name__ == '__main__':
  # Write your own test cases for your `play` function here.
  # These can be run with the Run button and will not affect the tournament or marking.

  # Here's an example test case and testing code to kick you off.
  TESTS = [  # [ expected return value, inputs ]
    #[['3D', '4D', '7D', '8D', '0D'], [['3D', '4D', '4H', '7D', '8D', '8H', '0D', '0C', 'JH', 'QC', 'QS', 'KH', 'AS'], True, [], [[]], 0, [13, 13, 13, 13], [0, 0, 0, 0], 0]],
    [['4H'], [['3D', '4D', '4H', '7D', '8D', '8H', '0D', '0C', 'JH', 'QC', 'QS', 'KH', 'AS'], False, ['4D', '4S'], [[]], 0, [13, 13, 13, 13], [0, 0, 0, 0], 0]],
    #[['8D', '8H'], [['3D', '4D', '4H', '7D', '8D', '8H', '0D', '0C', 'JH', 'QC', 'QS', 'KH', 'AS'], False, ['4D', '4H'], [[]], 0, [13, 13, 13, 13], [0, 0, 0, 0], 0]],
    #[[], [['3D', '4D', '4H', '7D', '8D', '8H', '0D', '0C', 'JH', 'QC', 'QS', 'KH', 'AS'], False, ['2S'], [[]], 0, [13, 13, 13, 13], [0, 0, 0, 0], 0]],
    #[['3D', '4D', '7D', '8D', '0D'], [['3D', '4D', '4H', '7D', '8D', '8H', '0D', '0C', 'JH', 'QC', 'QS', 'KH', 'AS'], False, [], [[]], 0, [13, 13, 13, 13], [0, 0, 0, 0], 0]],
    #[['3D', '3S'], [['3D', '3S', '4H', '7D', '8D', '8H', '0D', '0C', 'JH', 'QC', 'QS', 'KH', 'AS'], True, [], [[]], 0, [13, 13, 13, 13], [0, 0, 0, 0], 0]],
    #[['3D', '3C', '3S', 'QC', 'QS'], [['3D', '3S', '3C', '7D', '8D', '8H', '0D', '0C', 'JH', 'QC', 'QS', 'KH', 'AS'], True, [], [[]], 0, [13, 13, 13, 13], [0, 0, 0, 0], 0]],
    #[['3D', '4D', '5D', '6D', '7D'], [['3D', '3S', '3C', '4D', '5D', '8H', '6D', '7D', 'JH', 'QC', 'QS', 'KH', 'AS'], True, [], [[]], 0, [13, 13, 13, 13], [0, 0, 0, 0], 0]],
    # Add more tests here.
  ]

  # This runs the above test cases.
  for i, test in enumerate(TESTS):
    expected_return_value, inputs = test
    actual_return_value = play(*inputs)
    if actual_return_value == expected_return_value:
      print('PASSED {}/{}.'.format(i + 1, len(TESTS)))
    else:
      print('FAILED {}/{}.'.format(i + 1, len(TESTS)))
      print('    inputs:', repr(inputs))
      print('  expected:', repr(expected_return_value))
      print('    actual:', repr(actual_return_value))
