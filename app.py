import streamlit as st

# 1. 최상단 페이지 설정 (카톡 링크 제목 고정)
st.set_page_config(
    page_title="8인 테니스 단식 자동 관리", 
    page_icon="🎾", 
    layout="wide"
)

st.title("🎾 8인 테니스 단식 자동 관리")

# 2. 웹 메모장(session_state) 초기화
if 'step' not in st.session_state:
    st.session_state.step = 1  # 1: 등록, 2: 예선, 3: 본선, 4: 결과
if 'players' not in st.session_state:
    st.session_state.players = {'1조': [], '2조': [], '3조': []}
if 'group_results' not in st.session_state:
    st.session_state.group_results = {}
if 'match_results' not in st.session_state:
    st.session_state.match_results = {}

# --- [1단계: 조별 선수 명단 등록] ---
if st.session_state.step == 1:
    st.header("📋 1단계: 조별 선수 명단 등록")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("1조 (3명)")
        p1 = st.text_input("1조 1번 선수", value="선수A", key="g1_p1")
        p2 = st.text_input("1조 2번 선수", value="선수B", key="g1_p2")
        p3 = st.text_input("1조 3번 선수", value="선수C", key="g1_p3")
    with col2:
        st.subheader("2조 (3명)")
        p4 = st.text_input("2조 1번 선수", value="선수D", key="g2_p1")
        p5 = st.text_input("2조 2번 선수", value="선수E", key="g2_p2")
        p6 = st.text_input("2조 3번 선수", value="선수F", key="g2_p3")
    with col3:
        st.subheader("3조 (2명)")
        p7 = st.text_input("3조 1번 선수", value="선수G", key="g3_p1")
        p8 = st.text_input("3조 2번 선수", value="선수H", key="g3_p2")
        
    if st.button("선수 등록 완료 ➡️ 예선전 진행", type="primary"):
        st.session_state.players['1조'] = [p1, p2, p3]
        st.session_state.players['2조'] = [p4, p5, p6]
        st.session_state.players['3조'] = [p7, p8]
        st.session_state.step = 2
        st.rerun()

# --- [2단계: 조별 예선전 결과 입력] ---
elif st.session_state.step == 2:
    st.header("📋 조별 예선전 진행")
    
    group_matches = {
        '1조': [('1조 1경기', st.session_state.players['1조'][0], st.session_state.players['1조'][1]),
                ('1조 2경기', st.session_state.players['1조'][1], st.session_state.players['1조'][2]),
                ('1조 3경기', st.session_state.players['1조'][0], st.session_state.players['1조'][2])],
        '2조': [('2조 1경기', st.session_state.players['2조'][0], st.session_state.players['2조'][1]),
                ('2조 2경기', st.session_state.players['2조'][1], st.session_state.players['2조'][2]),
                ('2조 3경기', st.session_state.players['2조'][0], st.session_state.players['2조'][2])],
        '3조': [('3조 1경기', st.session_state.players['3조'][0], st.session_state.players['3조'][1])]
    }
    
    scores_input = {}
    cols = st.columns(3)
    
    for idx, (g_name, matches) in enumerate(group_matches.items()):
        with cols[idx]:
            st.subheader(f"🔹 {g_name} 예선")
            for m_key, p1, p2 in matches:
                st.markdown(f"**{p1} 🆚 {p2}**")
                s1 = st.number_input(f"{p1} 점수", min_value=0, max_value=10, value=6, key=f"{m_key}_s1")
                s2 = st.number_input(f"{p2} 점수", min_value=0, max_value=10, value=4, key=f"{m_key}_s2")
                
                if s1 == s2:
                    st.warning("⚠️ 테니스에는 무승부가 없습니다. 점수를 다르게 입력해주세요.")
                scores_input[m_key] = (p1, p2, s1, s2)
                st.markdown("---")
                
    if st.button("예선 결과 계산 ➡️ 8강 진출", type="primary"):
        # 순위 계산 및 검증
        has_tie = False
        for g_name in ['1조', '2조', '3조']:
            stats = {p: {'wins': 0, 'diff': 0} for p in st.session_state.players[g_name]}
            for m_key, p1, p2 in group_matches[g_name]:
                _, _, s1, s2 = scores_input[m_key]
                if s1 == s2:
                    has_tie = True
                if s1 > s2:
                    stats[p1]['wins'] += 1
                    stats[p1]['diff'] += (s1 - s2)
                    stats[p2]['diff'] += (s2 - s1)
                else:
                    stats[p2]['wins'] += 1
                    stats[p2]['diff'] += (s2 - s1)
                    stats[p1]['diff'] += (s1 - s2)
            
            ranked = sorted(st.session_state.players[g_name], key=lambda p: (stats[p]['wins'], stats[p]['diff']), reverse=True)
            st.session_state.group_results[g_name] = (ranked, stats)
            
        if has_tie:
            st.error("무승부 경기가 있습니다. 점수를 다시 확인해주세요.")
        else:
            st.session_state.step = 3
            st.rerun()

# --- [3단계: 본선 토너먼트 시작] ---
elif st.session_state.step == 3:
    st.header("🏆 본선 토너먼트 진행")
    
    # 예선 결과 불러오기
    g1_ranked, g1_stats = st.session_state.group_results['1조']
    g2_ranked, g2_stats = st.session_state.group_results['2조']
    g3_ranked, g3_stats = st.session_state.group_results['3조']
    
    # 조별 예선 결과 간략 요약 보여주기
    with st.expander("📊 조별 예선 최종 순위 결과 보기", expanded=False):
        for g_name, (ranked, stats) in st.session_state.group_results.items():
            st.write(f"**[{g_name} 결과]**")
            for idx, p in enumerate(ranked):
                st.write(f"{idx+1}위: {p} (승리: {stats[p]['wins']}, 득실차: {stats[p]['diff']})")
            st.write("")

    st.subheader("🎯 8강전")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"**1경기**\n\n{g1_ranked[0]} 🆚 {g3_ranked[1]}")
        qf1_s1 = st.number_input(f"{g1_ranked[0]}", min_value=0, value=6, key="qf1_s1")
        qf1_s2 = st.number_input(f"{g3_ranked[1]}", min_value=0, value=4, key="qf1_s2")
        qf1_w = g1_ranked[0] if qf1_s1 > qf1_s2 else g3_ranked[1]
        st.info(f"🎊 {qf1_w} 👉 4강 진출!!")
        
    with c2:
        st.markdown(f"**2경기**\n\n{g2_ranked[0]} 🆚 {g1_ranked[1]}")
        qf2_s1 = st.number_input(f"{g2_ranked[0]}", min_value=0, value=6, key="qf2_s1")
        qf2_s2 = st.number_input(f"{g1_ranked[1]}", min_value=0, value=4, key="qf2_s2")
        qf2_w = g2_ranked[0] if qf2_s1 > qf2_s2 else g1_ranked[1]
        st.info(f"🎊 {qf2_w} 👉 4강 진출!!")
        
    with c3:
        st.markdown(f"**3경기**\n\n{g1_ranked[2]} 🆚 {g2_ranked[2]}")
        qf3_s1 = st.number_input(f"{g1_ranked[2]}", min_value=0, value=6, key="qf3_s1")
        qf3_s2 = st.number_input(f"{g2_ranked[2]}", min_value=0, value=4, key="qf3_s2")
        qf3_w = g1_ranked[2] if qf3_s1 > qf3_s2 else g2_ranked[2]
        st.info(f"🎊 {qf3_w} 👉 4강 진출!!")
        
    with c4:
        st.markdown(f"**4경기**\n\n{g2_ranked[1]} 🆚 {g3_ranked[0]}")
        qf4_s1 = st.number_input(f"{g2_ranked[1]}", min_value=0, value=6, key="qf4_s1")
        qf4_s2 = st.number_input(f"{g3_ranked[0]}", min_value=0, value=4, key="qf4_s2")
        qf4_w = g2_ranked[1] if qf4_s1 > qf4_s2 else g3_ranked[0]
        st.info(f"🎊 {qf4_w} 👉 4강 진출!!")

    st.markdown("---")
    st.subheader("🔥 4강전")
    col_sf1, col_sf2 = st.columns(2)
    with col_sf1:
        st.markdown(f"**1경기**\n\n{qf1_w} 🆚 {qf3_w}")
        sf1_s1 = st.number_input(f"{qf1_w} 점수", min_value=0, value=6, key="sf1_s1")
        sf1_s2 = st.number_input(f"{qf3_w} 점수", min_value=0, value=4, key="sf1_s2")
        sf1_w = qf1_w if sf1_s1 > sf1_s2 else qf3_w
        sf1_l = qf3_w if sf1_s1 > sf1_s2 else qf1_w
        st.info(f"🎊 {sf1_w} 👉 결승 진출!!")
        
    with col_sf2:
        st.markdown(f"**2경기**\n\n{qf2_w} 🆚 {qf4_w}")
        sf2_s1 = st.number_input(f"{qf2_w} 점수", min_value=0, value=6, key="sf2_s1")
        sf2_s2 = st.number_input(f"{qf4_w} 점수", min_value=0, value=4, key="sf2_s2")
        sf2_w = qf2_w if sf2_s1 > sf2_s2 else qf4_w
        sf2_l = qf4_w if sf2_s1 > sf2_s2 else qf2_w
        st.info(f"🎊 {sf2_w} 👉 결승 진출!!")

    st.markdown("---")
    st.subheader("👑 순위 결정전 및 결승전")
    col_34, col_f = st.columns(2)
    with col_34:
        st.markdown(f"**🥉 3·4위전**\n\n{sf1_l} 🆚 {sf2_l}")
        t_s1 = st.number_input(f"{sf1_l} 점수 ",