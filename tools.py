from crewai_tools import BaseTool

class QuotationLogicTool(BaseTool):
    name: str = "Quotation Logic Tool"
    description: str = "비즈니스 규칙에 따라 가격을 계산하고 예외 상황을 감지합니다."

    def _run(self, word_count: int, difficulty: float) -> dict:
        base_rate = 120 # 원/단어
        final_price = word_count * base_rate * difficulty
        
        # 예외 처리: 데이터 오염 시
        if word_count <= 0:
            return {"error": "INVALID_WORD_COUNT", "price": 0}
            
        return {
            "price": int(final_price),
            "is_high_value": final_price >= 10000000,
            "requires_human_review": difficulty > 1.8 or final_price >= 10000000
        }