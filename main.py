import sys
from pydantic import BaseModel
from crewai.flow.flow import Flow, listen, start, router
from .crew import VoithruFactoryCrew

class VoithruState(BaseModel):
    client_email: str = ""
    quote_data: dict = {}
    is_approved: bool = False  # Human-in-the-loop용 상태
    error_msg: str = ""

class VoithruTranslationFlow(Flow[VoithruState]):

    @start()
    def fetch_and_analyze(self):
        print(">> Step 1: Gmail 검색 및 분석")
        result = VoithruFactoryCrew().crew().kickoff()
        # 실제 환경에선 result에서 email 정보를 파싱하여 state에 저장
        self.state.client_email = "client@example.com"
        return str(result)

    @router(fetch_and_analyze)
    def check_high_value(self):
        # 견적 결과에 따른 분기 로직
        if "REJECT" in self.state.error_msg:
            return "stop_and_report"
        return "slack_report"

    @listen("stop_and_report")
    def handle_exception(self):
        print(">> Exception: 알 수 없는 요청 또는 데이터 부족")
        # Slack 에이전트만 따로 호출하여 보고 가능
        return "Process Halted"

    @listen("slack_report")
    def notify_internal(self):
        print(">> Step 2: 내부 Slack 보고 및 승인 대기")
        # 실제 현업에선 여기서 대기하거나, 관리자 승인 로직(Webhook 등)을 연결
        self.state.is_approved = True # 테스트용 자동 승인
        return "Manager Notified via Slack"

    @listen(notify_internal)
    def send_final_quotation(self):
        if self.state.is_approved:
            print(f">> Step 3: 클라이언트({self.state.client_email})에게 최종 발송")
            # send_to_client_task 실행
            return "Project Completed Successfully"

def main():
    flow = VoithruTranslationFlow()
    flow.kickoff()

if __name__ == "__main__":
    main()