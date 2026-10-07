import streamlit as st
import chess
import chess.svg
import base64
from io import BytesIO

# ============================================================
# 페이지 설정
# ============================================================

st.set_page_config(
    page_title="Streamlit Chess",
    page_icon="♟️",
    layout="wide"
)

# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>
    .main {
        background-color: #f5f5f5;
    }

    .chess-title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .chess-subtitle {
        text-align: center;
        color: #666;
        margin-bottom: 25px;
    }

    .turn-box {
        padding: 15px;
        border-radius: 10px;
        background: white;
        border: 1px solid #ddd;
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 15px;
    }

    .move-box {
        background: white;
        border-radius: 10px;
        padding: 15px;
        border: 1px solid #ddd;
        max-height: 500px;
        overflow-y: auto;
    }

    .result-box {
        padding: 20px;
        border-radius: 12px;
        background: #fff3cd;
        border: 1px solid #ffeeba;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# 세션 상태 초기화
# ============================================================

if "board" not in st.session_state:
    st.session_state.board = chess.Board()

if "selected_square" not in st.session_state:
    st.session_state.selected_square = None

if "game_over" not in st.session_state:
    st.session_state.game_over = False


# ============================================================
# 체스판 SVG 생성
# ============================================================

def create_board_svg(board, selected_square=None):
    """
    현재 체스판을 SVG 이미지로 생성합니다.
    """

    arrows = []

    if selected_square is not None:
        legal_moves = [
            move for move in board.legal_moves
            if move.from_square == selected_square
        ]

        for move in legal_moves:
            arrows.append(
                chess.svg.Arrow(
                    selected_square,
                    move.to_square,
                    color="#22aa22"
                )
            )

    svg = chess.svg.board(
        board=board,
        size=650,
        coordinates=True,
        arrows=arrows
    )

    return svg


# ============================================================
# SVG를 화면에 표시
# ============================================================

def display_board(board, selected_square=None):
    svg = create_board_svg(board, selected_square)

    st.components.v1.html(
        svg,
        height=680,
        scrolling=False
    )


# ============================================================
# 새 게임
# ============================================================

def reset_game():
    st.session_state.board = chess.Board()
    st.session_state.selected_square = None
    st.session_state.game_over = False


# ============================================================
# 헤더
# ============================================================

st.markdown(
    '<div class="chess-title">♟️ Streamlit Chess</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="chess-subtitle">Python + Streamlit + python-chess</div>',
    unsafe_allow_html=True
)


# ============================================================
# 사이드바
# ============================================================

with st.sidebar:

    st.header("게임 설정")

    if st.button(
        "🔄 새 게임",
        use_container_width=True
    ):
        reset_game()
        st.rerun()

    st.divider()

    board = st.session_state.board

    st.subheader("게임 정보")

    if board.turn == chess.WHITE:
        turn_text = "⚪ 백색 차례"
    else:
        turn_text = "⚫ 흑색 차례"

    st.info(turn_text)

    st.write(
        f"**수(Number of moves):** {board.fullmove_number}"
    )

    st.write(
        f"**턴:** {'백' if board.turn else '흑'}"
    )

    st.divider()

    st.subheader("체스판")

    st.write("기물을 선택한 후 이동할 칸을 선택하세요.")

    st.divider()

    st.subheader("FEN")

    st.code(board.fen())


# ============================================================
# 메인 화면
# ============================================================

left, right = st.columns([2, 1])


# ============================================================
# 체스판 영역
# ============================================================

with left:

    board = st.session_state.board

    # 현재 차례 표시
    if board.turn == chess.WHITE:
        current_turn = "⚪ White's Turn"
    else:
        current_turn = "⚫ Black's Turn"

    st.markdown(
        f'<div class="turn-box">{current_turn}</div>',
        unsafe_allow_html=True
    )

    # 체크 상태
    if board.is_check() and not board.is_game_over():
        st.warning("⚠️ 체크!")

    # 게임 종료
    if board.is_checkmate():

        winner = "흑색" if board.turn == chess.WHITE else "백색"

        st.markdown(
            f"""
            <div class="result-box">
                🏆 체크메이트!<br>
                {winner} 승리
            </div>
            """,
            unsafe_allow_html=True
        )

        st.session_state.game_over = True

    elif board.is_stalemate():

        st.markdown(
            """
            <div class="result-box">
                🤝 스테일메이트<br>
                무승부
            </div>
            """,
            unsafe_allow_html=True
        )

        st.session_state.game_over = True

    elif board.is_insufficient_material():

        st.markdown(
            """
            <div class="result-box">
                🤝 기물 부족<br>
                무승부
            </div>
            """,
            unsafe_allow_html=True
        )

        st.session_state.game_over = True

    # ========================================================
    # 체스판 표시
    # ========================================================

    display_board(
        board,
        st.session_state.selected_square
    )


# ============================================================
# 게임 정보 영역
# ============================================================

with right:

    st.subheader("📜 게임 상태")

    board = st.session_state.board

    if board.is_checkmate():
        st.error("체크메이트")

    elif board.is_stalemate():
        st.warning("스테일메이트")

    elif board.is_check():
        st.warning("체크")

    else:
        st.success("게임 진행 중")

    st.divider()

    st.subheader("♟️ 현재 기물")

    piece_count = {
        "백 킹": 0,
        "백 퀸": 0,
        "백 룩": 0,
        "백 비숍": 0,
        "백 나이트": 0,
        "백 폰": 0,
        "흑 킹": 0,
        "흑 퀸": 0,
        "흑 룩": 0,
        "흑 비숍": 0,
        "흑 나이트": 0,
        "흑 폰": 0,
    }

    piece_names = {
        chess.KING: "킹",
        chess.QUEEN: "퀸",
        chess.ROOK: "룩",
        chess.BISHOP: "비숍",
        chess.KNIGHT: "나이트",
        chess.PAWN: "폰",
    }

    for square, piece in board.piece_map().items():

        color = "백" if piece.color == chess.WHITE else "흑"
        name = piece_names[piece.piece_type]

        key = f"{color} {name}"

        if key in piece_count:
            piece_count[key] += 1

    for name, count in piece_count.items():

        if count > 0:
            st.write(f"{name}: **{count}**")

    st.divider()

    st.subheader("📖 수순")

    if board.move_stack:

        history = []

        temp_board = chess.Board()

        for i, move in enumerate(board.move_stack):

            move_number = temp_board.fullmove_number
            san = temp_board.san(move)

            if temp_board.turn == chess.WHITE:
                history.append(
                    f"{move_number}. {san}"
                )
            else:
                history[-1] += f" {san}"

            temp_board.push(move)

        for move in history:
            st.write(move)

    else:
        st.caption("아직 진행된 수가 없습니다.")


# ============================================================
# 사용 방법
# ============================================================

st.divider()

st.subheader("🎮 플레이 방법")

st.markdown("""
1. 체스판에서 움직일 기물을 선택합니다.
2. 이동 가능한 칸을 확인합니다.
3. 원하는 위치로 이동합니다.
4. 모든 체스 규칙은 `python-chess`가 검사합니다.
5. 체크메이트가 발생하면 게임이 종료됩니다.

### 지원되는 주요 체스 규칙

- 일반 기물 이동
- 기물 잡기
- 체크
- 체크메이트
- 스테일메이트
- 캐슬링
- 앙파상
- 폰 프로모션
- 합법적인 수 검사
""")
