from .utils import assign_group
import random

class ABTestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # session에 그룹 정보가 없다면 
        if "ab_group" not in request.session:
            # 회원 => id, 비회원 => 랜덤 번호로 그룹 할당 (A/B)
            user_identifier = request.user.id if request.user.is_authenticated else random.randint(1, 999999)
            request.session["ab_group"] = assign_group(user_identifier)
            # 그룹 지정된 정보를 응답으로 
        response = self.get_response(request)
        return response