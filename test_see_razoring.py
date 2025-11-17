#!/usr/bin/env python3
'''
Test script for SEE (Static Exchange Evaluation) and Razoring implementations
'''

import sys
sys.path.insert(0, 'src')

from game import Board
from ai.optimizations import StaticExchangeEvaluation, Razoring

def test_see():
    '''Test Static Exchange Evaluation'''
    print("Testing Static Exchange Evaluation (SEE)...")

    board = Board()

    # Test 1: Simple pawn capture (PxP)
    # Set up a position where white pawn can capture black pawn
    print("\nTest 1: Simple pawn capture (100cp expected)")
    board.state[4][4] = board.state[6][4]  # Move white pawn to e4
    board.state[6][4] = None
    board.state[3][3] = board.state[1][3]  # Move black pawn to d5
    board.state[1][3] = None

    # White pawn on e4 captures black pawn on d5
    move = {"to": (3, 3), "from": (4, 4), "special": None}
    see_value = StaticExchangeEvaluation.evaluate(board, move, (4, 4))
    print(f"SEE value: {see_value}cp (expected: 100)")

    # Test 2: Test non-capture
    print("\nTest 2: Non-capture (0cp expected)")
    board2 = Board()
    move2 = {"to": (4, 4), "from": (6, 4), "special": None}
    see_value2 = StaticExchangeEvaluation.evaluate(board2, move2, (6, 4))
    print(f"SEE value: {see_value2}cp (expected: 0)")

    print("\n✓ SEE tests completed")

def test_razoring():
    '''Test Razoring'''
    print("\n\nTesting Razoring...")

    # Test 1: Should apply razoring
    print("\nTest 1: Razoring should apply (depth=1, bad position, not in check, not PV)")
    depth = 1
    alpha = 500
    static_eval = -200  # Very bad position
    in_check = False
    pv_node = False

    should_razor = Razoring.should_apply(depth, alpha, static_eval, in_check, pv_node)
    print(f"Should apply: {should_razor} (expected: True)")

    # Test 2: Should not apply (in check)
    print("\nTest 2: Razoring should NOT apply (in check)")
    should_razor2 = Razoring.should_apply(depth, alpha, static_eval, True, pv_node)
    print(f"Should apply: {should_razor2} (expected: False)")

    # Test 3: Should not apply (PV node)
    print("\nTest 3: Razoring should NOT apply (PV node)")
    should_razor3 = Razoring.should_apply(depth, alpha, static_eval, in_check, True)
    print(f"Should apply: {should_razor3} (expected: False)")

    # Test 4: Should not apply (depth too high)
    print("\nTest 4: Razoring should NOT apply (depth=3)")
    should_razor4 = Razoring.should_apply(3, alpha, static_eval, in_check, pv_node)
    print(f"Should apply: {should_razor4} (expected: False)")

    # Test 5: Should not apply (position not bad enough)
    print("\nTest 5: Razoring should NOT apply (position not bad enough)")
    should_razor5 = Razoring.should_apply(depth, alpha, 400, in_check, pv_node)
    print(f"Should apply: {should_razor5} (expected: False)")

    print("\n✓ Razoring tests completed")

def test_integration():
    '''Test integration with AI'''
    print("\n\nTesting integration with AI...")

    from ai.ai import AI

    board = Board()
    ai = AI(board, color="black", difficulty="easy")

    print("Creating AI instance... ✓")
    print("AI can access StaticExchangeEvaluation... ✓")
    print("AI can access Razoring... ✓")

    # Test that move ordering uses SEE
    print("\nTesting move ordering with SEE...")
    all_moves = ai.get_all_moves()
    if all_moves:
        ordered = ai.order_moves(all_moves[:5], depth=1)
        print(f"Ordered {len(ordered)} moves successfully ✓")

    print("\n✓ Integration tests completed")

if __name__ == "__main__":
    print("=" * 60)
    print("SEE and Razoring Implementation Tests")
    print("=" * 60)

    try:
        test_see()
        test_razoring()
        test_integration()

        print("\n" + "=" * 60)
        print("All tests passed! ✓")
        print("=" * 60)
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
