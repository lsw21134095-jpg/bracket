def play_score_match(match_name, p1, p2):
    """점수를 입력받아 승자와 패자, 득점을 반환하는 함수"""
    print(f"\n▶ [{match_name}] {p1} 🆚 {p2}")
    while True:
        try:
            # "6 4"와 같이 띄어쓰기로 점수 입력
            score = input(f"👉 {p1}와(과) {p2}의 획득 게임 수를 입력하세요 (예: 6 4) : ").split()
            if len(score) != 2:
                raise ValueError
            
            s1, s2 = int(score[0]), int(score[1])
            
            if s1 > s2:
                print(f"🎉 {p1} 승리! ({s1}:{s2})")
                return p1, p2, s1, s2
            elif s2 > s1:
                print(f"🎉 {p2} 승리! ({s2}:{s1})")
                return p2, p1, s2, s1
            else:
                print("⚠️ 테니스에는 무승부가 없습니다. 점수를 다시 입력해주세요.")
        except ValueError:
            print("⚠️ 올바른 형식으로 점수를 띄어쓰기로 구분하여 입력해주세요 (예: 6 4).")

def rank_group(group_name, players):
    """조별 예선전을 진행하고 순위를 반환하는 함수"""
    print(f"\n" + "="*40)
    print(f"📋 [{group_name} 예선전 진행]")
    print("="*40)
    
    # 선수별 성적 기록 딕셔너리 (승수, 게임 득실차)
    stats = {p: {'wins': 0, 'diff': 0} for p in players}
    
    # 3명이면 풀리그(3경기), 2명이면 맞대결(1경기)
    matches = [(0, 1), (1, 2), (0, 2)] if len(players) == 3 else [(0, 1)]
    
    for i, j in matches:
        p1, p2 = players[i], players[j]
        winner, loser, win_score, lose_score = play_score_match(f"{group_name} 예선", p1, p2)
        
        # 승자/패자 스탯 업데이트
        stats[winner]['wins'] += 1
        stats[winner]['diff'] += (win_score - lose_score)
        stats[loser]['diff'] += (lose_score - win_score)
        
    # 순위 정렬: 1순위(다승), 2순위(득실차 높은 순)
    ranked = sorted(players, key=lambda p: (stats[p]['wins'], stats[p]['diff']), reverse=True)
    
    print(f"\n📊 [{group_name} 최종 순위 결과]")
    for idx, p in enumerate(ranked):
        print(f"{idx+1}위: {p} (승리: {stats[p]['wins']}, 득실차: {stats[p]['diff']})")
        
    return ranked

def main():
    print("="*50)
    print("🎾 8인 테니스 단식 대회 자동 관리 프로그램 🎾")
    print("="*50)

    # 1. 선수 명단 입력
    print("\n[1단계: 조별 선수 명단 등록]")
    g1_players = [input(f"1조 {i}번 선수 이름: ") for i in range(1, 4)]
    print("-" * 20)
    g2_players = [input(f"2조 {i}번 선수 이름: ") for i in range(1, 4)]
    print("-" * 20)
    g3_players = [input(f"3조 {i}번 선수 이름: ") for i in range(1, 3)]

    # 2. 조별 예선 진행 및 순위 자동 계산
    g1_ranked = rank_group("1조", g1_players)
    g2_ranked = rank_group("2조", g2_players)
    g3_ranked = rank_group("3조", g3_players)

    # 3. 본선 8강 진행
    print("\n" + "="*50)
    print("🏆 [본선 8강전 토너먼트 시작]")
    print("="*50)
    
    qf1_w, _, _, _ = play_score_match("8강 1경기", g1_ranked[0], g3_ranked[1]) # 1조 1위 vs 3조 2위
    qf2_w, _, _, _ = play_score_match("8강 2경기", g2_ranked[0], g1_ranked[1]) # 2조 1위 vs 1조 2위
    qf3_w, _, _, _ = play_score_match("8강 3경기", g1_ranked[2], g2_ranked[2]) # 1조 3위 vs 2조 3위
    qf4_w, _, _, _ = play_score_match("8강 4경기", g2_ranked[1], g3_ranked[0]) # 2조 2위 vs 3조 1위

    # 4. 본선 4강 진행
    print("\n" + "="*50)
    print("🔥 [본선 4강전 시작]")
    print("="*50)
    
    sf1_w, sf1_l, _, _ = play_score_match("4강 1경기", qf1_w, qf3_w)
    sf2_w, sf2_l, _, _ = play_score_match("4강 2경기", qf2_w, qf4_w)

    # 5. 3·4위전 및 결승전 진행
    print("\n" + "="*50)
    print("👑 [순위 결정전 및 결승전 시작]")
    print("="*50)
    
    third_w, third_l, _, _ = play_score_match("3·4위전", sf1_l, sf2_l)
    final_w, final_l, _, _ = play_score_match("결승전", sf1_w, sf2_w)

    # 6. 최종 결과 출력
    print("\n" + "="*50)
    print("🎊 [대회 최종 결과] 🎊")
    print("="*50)
    print(f"🥇 우승   : {final_w}")
    print(f"🥈 준우승 : {final_l}")
    print(f"🥉 3위    : {third_w}")
    print(f"🎖️ 4위    : {third_l}")
    print("="*50)
    print("수고하셨습니다! 대회가 종료되었습니다.")

if __name__ == "__main__":
    main()