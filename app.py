import streamlit as st

st.set_page_config(page_title="8인 테니스 대회 관리 시스템", page_icon="🎾", layout="wide")

st.title("🎾 8인 테니스 단식 대회 자동 관리 시스템")

# 1. 웹 메모장(session_state) 초기화 - 새로고침되어도 데이터 유지
if 'step' not in st.session_state:
    st.session_state.step = 1  # 1: 선수등록, 2: 예선진행, 3: 본선토너먼트, 4: 최종결과
if 'players' not in st.session_state:
    st.session_state.players = {'1조': [], '2조': [], '3조': []}
if 'group_results' not in st.session_state:
    st.session_state.group_results = {}
if 'match_results' not in st.session_state:
    st.session_state.match_results = {}

# --- [1단계: 선수 명단 등록] ---
if st.session_state.step == 1:
    st.header("📋 1단계: 조별 선수 명단 등록")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("1조 (3명)")
        p1 = st.text_input("1조 1번 선수", value="선수A")
        p2 = st.text_input("1조 2번 선수", value="선수B")
        p3 = st.text_input("1조 3번 선수", value="선수C")
        
    with col2:
        st.subheader("2조 (3명)")
        p4 = st.text_input("2조 1번 선수", value="선수D")
        p5 = st.text_input("2조 2번 선수", value="선수E")
        p6 = st.text_input("2조 3번 선수", value="선수F")
        
    with col3:
        st.subheader("3조 (2명)")
        p7 = st.text_input("3조 1번 선수", value="선수G")
        p8 = st.text_input("3조 2번 선수", value="선수H")
        
    if st.button("선수 등록 완료 ➡️ 예선전 진행"):
        st.session_state.players['1조'] = [p1, p2, p3]
        st.session_state.players['2조'] = [p4, p5, p6]
        st.session_state.players['3조'] = [p7, p8]
        st.session_state.step = 2
        st.rerun()

# --- [2단계: 조별 예선전 점수 입력] ---
elif st.session_state.step == 2:
    st.header("📊 2단계: 조별 예선전 결과 입력")
    st.write("각 경기의 획득 게임 수를 입력해 주세요.")
    
    # 예선 대진표 구성
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
    
    # 화면을 3개 조로 분할 표시
    cols = st.columns(3)
    for idx, (g_name, matches) in enumerate(group_matches.items()):
        with cols[idx]:
            st.subheader(f"🔹 {g_name}")
            for m_key, p1, p2 in matches:
                st.write(f"▶ {p1} 🆚 {p2}")
                s1 = st.number_input(f"{p1} 게임 수", min_value=0, max_value=10, value=6, key=f"{m_key}_s1")
                s2 = st.number_input(f"{p2} 게임 수", min_value=0, max_value=10, value=4, key=f"{m_key}_s2")
                scores_input[m_key] = (p1, p2, s1, s2)
                st.markdown("---")
                
    if st.button("예선 결과 계산 ➡️ 8강 토너먼트 진출"):
        # 순위 계산 로직
        for g_name in ['1조', '2조', '3조']:
            stats = {p: {'wins': 0, 'diff': 0} for p in st.session_state.players[g_name]}
            
            for m_key, p1, p2 in group_matches[g_name]:
                _, _, s1, s2 = scores_input[m_key]
                if s1 > s2:
                    stats[p1]['wins'] += 1
                    stats[p1]['diff'] += (s1 - s2)
                    stats[p2]['diff'] += (s2 - s1)
                else:
                    stats[p2]['wins'] += 1
                    stats[p2]['diff'] += (s2 - s1)
                    stats[p1]['diff'] += (s1 - s2)
                    
            # 가나다순이 아닌 다승 및 득실차 순 정렬
            ranked = sorted(st.session_state.players[g_name], key=lambda p: (stats[p]['wins'], stats[p]['diff']), reverse=True)
            st.session_state.group_results[g_name] = ranked
            
        st.session_state.step = 3
        st.rerun()

# --- [3단계: 본선 토너먼트 (8강, 4강, 결승)] ---
elif st.session_state.step == 3:
    st.header("🏆 3단계: 본선 토너먼트")
    
    g1 = st.session_state.group_results['1조']
    g2 = st.session_state.group_results['2조']
    g3 = st.session_state.group_results['3조']
    
    st.subheader("🎯 8강전 대진 및 결과 입력")
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.write(f"1경기: {g1[0]} (1조1위) 🆚 {g3[1]} (3조2위)")
        qf1_s1 = st.number_input(f"{g1[0]} 점수", min_value=0, value=6, key="qf1_1")
        qf1_s2 = st.number_input(f"{g3[1]} 점수", min_value=0, value=4, key="qf1_2")
        qf1_w = g1[0] if qf1_s1 > qf1_s2 else g3[1]
        
    with c2:
        st.write(f"2경기: {g2[0]} (2조1위) 🆚 {g1[1]} (1조2위)")
        qf2_s1 = st.number_input(f"{g2[0]} 점수", min_value=0, value=6, key="qf2_1")
        qf2_s2 = st.number_input(f"{g1[1]} 점수", min_value=0, value=4, key="qf2_2")
        qf2_w = g2[0] if qf2_s1 > qf2_s2 else g1[1]
        
    with c3:
        st.write(f"3경기: {g1[2]} (1조3위) 🆚 {g2[2]} (2조3위)")
        qf3_s1 = st.number_input(f"{g1[2]} 점수", min_value=0, value=6, key="qf3_1")
        qf3_s2 = st.number_input(f"{g2[2]} 점수", min_value=0, value=4, key="qf3_2")
        qf3_w = g1[2] if qf3_s1 > qf3_s2 else g2[2]
        
    with c4:
        st.write(f"4경기: {g2[1]} (2조2위) 🆚 {g3[0]} (3조1위)")
        qf4_s1 = st.number_input(f"{g2[1]} 점수", min_value=0, value=6, key="qf4_1")
        qf4_s2 = st.number_input(f"{g3[0]} 점수", min_value=0, value=4, key="qf4_2")
        qf4_w = g2[1] if qf4_s1 > qf4_s2 else g3[0]

    st.markdown("---")
    st.subheader("🔥 4강전 결과 입력")
    col_sf1, col_sf2 = st.columns(2)
    
    with col_sf1:
        st.write(f"4강 1경기: {qf1_w} 🆚 {qf3_w}")
        sf1_s1 = st.number_input(f"{qf1_w} 점수", min_value=0, value=6, key="sf1_1")
        sf2_s2 = st.number_input(f"{qf3_w} 점수", min_value=0, value=4, key="sf1_2")
        sf1_w = qf1_w if sf1_s1 > sf2_s2 else qf3_w
        sf1_l = qf3_w if sf1_s1 > sf2_s2 else qf1_w
        
    with col_sf2:
        st.write(f"4강 2경기: {qf2_w} 🆚 {qf4_w}")
        sf2_s1 = st.number_input(f"{qf2_w} 점수", min_value=0, value=6, key="sf2_1")
        sf2_s2 = st.number_input(f"{qf4_w} 점수", min_value=0, value=4, key="sf2_2")
        sf2_w = qf2_w if sf2_s1 > sf2_s2 else qf4_w
        sf2_l = qf4_w if sf2_s1 > sf2_s2 else qf2_w

    st.markdown("---")
    st.subheader("👑 결승전 및 3·4위전 결과 입력")
    col_f, col_34 = st.columns(2)
    
    with col_34:
        st.write(f"🥉 3·4위전: {sf1_l} 🆚 {sf2_l}")
        t_s1 = st.number_input(f"{sf1_l} 점수", min_value=0, value=6, key="t_1")
        t_s2 = st.number_input(f"{sf2_l} 점수", min_value=0, value=4, key="t_2")
        third_place = sf1_l if t_s1 > t_s2 else sf2_l
        fourth_place = sf2_l if t_s1 > t_s2 else sf1_l
        
    with col_f:
        st.write(f"🥇 결승전: {sf1_w} 🆚 {sf2_w}")
        f_s1 = st.number_input(f"{sf1_w} 점수", min_value=0, value=6, key="f_1")
        f_s2 = st.number_input(f"{sf2_w} 점수", min_value=0, value=4, key="f_2")
        winner = sf1_w if f_s1 > f_s2 else sf2_w
        runner_up = sf2_w if f_s1 > f_s2 else sf1_w

    if st.button("대회 종료 ➡️ 최종 결과 보기"):
        st.session_state.match_results = {
            '1위': winner, '2위': runner_up, '3위': third_place, '4위': fourth_place
        }
        st.session_state.step = 4
        st.rerun()

# --- [4단계: 최종 결과 출력 및 리셋] ---
elif st.session_state.step == 4:
    st.balloons()
    st.header("🎊 [대회 최종 결과] 🎊")
    
    res = st.session_state.match_results
    st.markdown(f"### 🥇 우승 : {res['1위']}")
    st.markdown(f"### 🥈 준우승 : {res['2위']}")
    st.markdown(f"### 🥉 3위 : {res['3위']}")
    st.markdown(f"### 🎖️ 4위 : {res['4위']}")
    
    if st.button("새 대회 시작하기 (처음으로)"):
        st.session_state.clear()
        st.rerun()