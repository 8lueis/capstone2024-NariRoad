import random

# A/B TEST - 그룹 분할(UI에 따른 사용자 행동 분석 위함)
def assign_group(user_identifier):
    random.seed(user_identifier)
    return "A" if random.random() < 0.5 else "B"