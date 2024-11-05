import re
import pandas as pd

# 예제 데이터 (텍스트 파일에서 데이터를 읽어올 경우 이 부분은 생략 가능)
data = """
---------------------------------------------------------------------------------------------------------------------------------------------------------------
 디바이스명 | 장애구분 | 코드 (구분코드 2~3 byte + 에러코드 5 byte)
------------+----------+----------------------------------------------------------------------
OP          | I        | OP11111 - 관리자 로그인
OP          | I        | OP11111 - 관리자 로그아웃
------------+----------+----------------------------------------------------------------------
OP          | I        | OP22222 - 현송사 로그인
OP          | I        | OP22222 - 현송사 로그아웃
------------+----------+----------------------------------------------------------------------
PRINTER     | E        | POP00001 - 프린터가 오프라인이거나 전원이 들어오지 않습니다.
            | E        | POP00002 - 일치하지 않는 라이브러리
            | E        | POP00003 - 프린터 헤드가 열렸습니다.
            | E        | POP00004 - 커터가 재설정되지 않았습니다.
            | E        | POP00005 - 프린터 헤드 온도가 비정상적입니다.
            | E        | POP00006 - 프린터가 블랙마크를 감지하지 못합니다.
            | E        | POP00007 - 용지 없음
            | E        | POP00008 - 용지 부족
------------+----------+----------------------------------------------------------------------
PRINTER     | E        | PTR00001 - 프린터가 오프라인이거나 전원이 들어오지 않습니다.
            | E        | PTR00002 - 일치하지 않는 라이브러리
            | E        | PTR00003 - 현재 프린터는 특수 기능을 지원할 수 없습니다
            | E        | PTR00004 - 프린터가 presenter에 용지를 로드하지 않습니다.
            | E        | PTR00005 - 프린터 베젤에 용지가 걸렸습니다.
            | E        | PTR00006 - 프린터 메커니즘에 용지 걸림
            | E        | PTR00007 - 완성되지 않은 티켓이 외부의 힘에 의해 끌려갑니다.
            | E        | PTR00008 - 프린터 베젤에 티켓이 있습니다
------------+----------+----------------------------------------------------------------------
CAMERA1     | E        | CAM00000  - 카메라 명령처리 에러
            | E        | CAM00001  - 지정된 카메라 없음
            | E        | CAM00002  - ImageEncoder 생성 오류
            | E        | CAM00003  - DirectShow HResult 오류
            | E        | CAM00004  - 이미지버퍼 생성 오류
            | E        | CAM00005  - ImageCodec  오류
            | E        | CAM00006  - 카메라 영상 GrabData 오류
            | E        | CAM00007  - HANDLE 오류
            | E        | CAM00008  - 이미지 저장 오류
            | E        | CAM00009  - 카메라 인덱스 오류
            | E        | CAM00010  - 카메라 연결 끊김
------------+----------+----------------------------------------------------------------------
CAMERA2     | E        | CAM00000  - 카메라 명령처리 에러
            | E        | CAM00001  - 지정된 카메라 없음
            | E        | CAM00002  - ImageEncoder 생성 오류
            | E        | CAM00003  - DirectShow HResult 오류
            | E        | CAM00004  - 이미지버퍼 생성 오류
            | E        | CAM00005  - ImageCodec  오류
            | E        | CAM00006  - 카메라 영상 GrabData 오류
            | E        | CAM00007  - HANDLE 오류
            | E        | CAM00008  - 이미지 저장 오류
            | E        | CAM00009  - 카메라 인덱스 오류
            | E        | CAM00010  - 카메라 연결 끊김
------------+----------+----------------------------------------------------------------------
CAMERA3     | E        | CAM00000  - 카메라 명령처리 에러
            | E        | CAM00001  - 지정된 카메라 없음
            | E        | CAM00002  - ImageEncoder 생성 오류
            | E        | CAM00003  - DirectShow HResult 오류
            | E        | CAM00004  - 이미지버퍼 생성 오류
            | E        | CAM00005  - ImageCodec  오류
            | E        | CAM00006  - 카메라 영상 GrabData 오류
            | E        | CAM00007  - HANDLE 오류
            | E        | CAM00008  - 이미지 저장 오류
            | E        | CAM00009  - 카메라 인덱스 오류
            | E        | CAM00010  - 카메라 연결 끊김
------------+----------+----------------------------------------------------------------------
RECYCLER    | E        | RAL00001   장비에 통신이 연결되어 있지 않음
            | E        | RAL00002   명령 전송에 실패함
            | E        | RAL00003   명령에 대한 Response 시간 초과
            | E        | RAL00004   이전 명령에 대한 Response 대기 중
            | E        | RAL00005   유효하지 않은 파라미터
------------+----------+----------------------------------------------------------------------
RECYCLER    | E        | RML00001  장비에 Error 가 있어 명령이 수행될 수 없음
            | E        | RML00002  내부 통신 실패 SC 간 통신 실패
            | E        | RML00003  다른 처리 수행 중으로 명령을 수행할 수 없음
            | E        | RML00004  다른 처리 모드 상태로 현재 명령을 수행 할 수 없음
            | E        | RML00005  사용자가 장비 UI 를 통해 설정 매뉴로 진입해 있음
            | E        | RML00006  명령과 함께 전송된 데이터가 유효하지 않음
            | E        | RML00007  설정 적용 실패
            | E        | RML00008  설정 읽기 실패
            | E        | RML00009  내부 통신 실패 Reco 간 통신 실패
            | E        | RML00010  명령을 수행할 수 없는 모드 상태에 있음
            | E        | RML00011  Hopper에 지폐가 있어 명령을 수행할 수 없음
            | E        | RML00012  돈이 부족함
            | E        | RML00013  명령을 수행하기 적합한 Currency 가 아님
------------+----------+----------------------------------------------------------------------
RECYCLER    | E        | RMS_00002  errorString: 모터 부하 발생 장애                      [Description("모터 구동 중 일정 수준 이상의 부하가 발생함")]
            | E        | RMS_00004  errorString: 상단 레일 열림 장애                      [Description("상단 레일이 열려 있습니다. 레일을 닫아주세요.")]
            | E        | RMS_00006  errorString: 장애 발생 후 호퍼 센서부에 지폐 감지됨   [Description("오류가 발생한 후 호퍼센서에 지폐가 걸려있습니다. 호퍼에 걸린 지폐를 제거해 주세요.")]
            | E        | RMS_00008  errorString: Insert Sensor 위치 지폐 걸림             [Description("Insert Sensor 위치에 지폐가 끼어있는지 확인 후, 삽입센서에 지폐가 끼임 지폐를 꺼내주세요.")]
            | E        | RMS_00009  errorString: Separate Sensor 지폐 걸림                [Description("지폐가 Separate Sensor에 걸렸습니다. 지폐가 별도 센서에 걸렸는지 확인하세요. 확인 후 지폐를 꺼내주세요.")]
            | E        | RMS_00010  errorString: RejectCount Sensor 지폐 걸림             [Description("RejectCount Sensor에 지폐가 있습니다. 지폐가 있는지 확인하신 후 꺼내주세요.")]
            | E        | RMS_00013  errorString: Deposit Count Sensor 지폐 걸림           [Description("Deposit Count Sensor에 지폐가 걸려있습니다. 지폐가 붙어 있는지 확인 후 꺼내주세요.")]
            | E        | RMS_00014  errorString: 반환부 지폐 존재                         [Description("Error 발생 후 Reject 포켓에 지폐가 남아 있습니다. Reject Pocket에서 지폐를 제거해주세요.")]
            | E        | RMS_00015  errorString: SC와 RECO 통신 오류                      [Description("SC와 RECO 사이에 통신 오류가 발생했습니다.")]
            | E        | RMS_00016  errorString: RECO와 FPGA 통신 오류                    [Description("RECO와 FPGA 사이에 통신 오류가 있습니다.")]
            | E        | RMS_00019  errorString: 금고 문 열림                             [Description("금고 문이 열려 있습니다.")]
            | E        | RMS_00024  errorString: 금고 카세트 미장착                       [Description("금고에 카세트가 장착되어 있지 않습니다.")]
            | E        | RMS_00033  errorString: 카세트의 푸시 장애                       [Description("카세트의 푸시 작업에 문제가 있습니다.")]
            | E        | RMS_00034  errorString: Jam Sensor 지폐 걸림                     [Description("Jam Sensor에 지폐가 걸렸습니다. Jam Sensor에서 지폐 확인 후 제거해주세요.")]
            | E        | RMS_00035  errorString: Enter Sensor 지폐 걸림                   [Description("Enter Sensor에 지폐가 끼어 있습니다. Enter Sensor에서 지폐 확인 후 제거해주세요.")]
            | E        | RMS_00036  errorString: Cassette Count Sensor 지폐 걸림          [Description("지폐가 Cassette Count Sensor에 걸렸습니다. Cassette Count Sensor 내 지폐를 확인하신 후 꺼내주세요.")]
            | E        | RMS_00038  errorString: Lower Path Sensor 지폐 걸림              [Description("Lower Path Sensor에 지폐가 걸렸습니다. Lower Path Sensor에서 지폐확인 후 지폐를 꺼내주세요.")]
            | E        | RMS_00039  errorString: Lower Sensor1 지폐 걸림                  [Description("Lower Sensor1에 지폐가 걸렸습니다. Lower Sensor1에서 지폐 확인 후 지폐를 꺼내주세요.")]
            | E        | RMS_00040  errorString: Lower Sensor2 지폐 걸림                  [Description("Lower Sensor2에 지폐가 걸렸습니다. Lower Sensor2에서 지폐 확인 후 지폐를 꺼내주세요.")]
            | E        | RMS_00041  errorString: Lower Sensor3 지폐 걸림                  [Description("Lower Sensor3에 지폐가 걸렸습니다. Lower Sensor3에서 지폐 확인 후 지폐를 꺼내주세요.")]
            | E        | RMS_00042  errorString: Drum Sensor1 지폐 걸림                   [Description("Drum Sensor1에 지폐가 걸렸습니다. Drum Sensor1에서 지폐를 확인한 후 지폐를 꺼내주세요.")]
            | E        | RMS_00043  errorString: Drum Sensor2 지폐 걸림                   [Description("Drum Sensor2에 지폐가 걸렸습니다. Drum Sensor2에서 지폐를 확인한 후 지폐를 꺼내주세요.")]
            | E        | RMS_00044  errorString: Drum Sensor3 지폐 걸림                   [Description("Drum Sensor3에 지폐가 걸렸습니다. Drum Sensor3에서 지폐를 확인한 후 지폐를 꺼내주세요.")]
            | E        | RMS_00045  errorString: Drum Sensor4 지폐 걸림                   [Description("Drum Sensor4에 지폐가 걸렸습니다. Drum Sensor4에서 지폐를 확인한 후 지폐를 꺼내주세요.")]
            | E        | RMS_00047  errorString: Lower Rail 열림 장애                     [Description("Lower Rail이 열려 있습니다. Lower Rail이 열려 있는지 확인하세요.")]
            | E        | RMS_00048  errorString: Drum1 Full 장애                          [Description("Drum1 가득 참. Drum1 의 필름 끝이 감지되어 드럼에 지폐가 더 이상 들어갈 수 없거나, 지폐가 제대로 쌓이지 않아 더 이상 지폐를 넣을 수 없습니다. 뭉쳐져 있는 지폐를 꺼내주세요.")]
            | E        | RMS_00049  errorString: Drum2 Full 장애                          [Description("Drum2 가득 참. Drum2 의 필름 끝이 감지되어 드럼에 지폐가 더 이상 들어갈 수 없거나, 지폐가 제대로 쌓이지 않아 더 이상 지폐를 넣을 수 없습니다. 뭉쳐져 있는 지폐를 꺼내주세요.")]
            | E        | RMS_00050  errorString: Drum3 Full 장애                          [Description("Drum3 가득 참. Drum3 의 필름 끝이 감지되어 드럼에 지폐가 더 이상 들어갈 수 없거나, 지폐가 제대로 쌓이지 않아 더 이상 지폐를 넣을 수 없습니다. 뭉쳐져 있는 지폐를 꺼내주세요.")]
            | E        | RMS_00051  errorString: Drum4 Full 장애                          [Description("Drum4 가득 참. Drum4 의 필름 끝이 감지되어 드럼에 지폐가 더 이상 들어갈 수 없거나, 지폐가 제대로 쌓이지 않아 더 이상 지폐를 넣을 수 없습니다. 뭉쳐져 있는 지폐를 꺼내주세요.")]
            | E        | RMS_00052  errorString: L-Main Motor 장애                        [Description("L-Main Motor가 회전하지 않거나 Encoder 신호가 없습니다.")]
            | E        | RMS_00053  errorString: Drum1 Motor 또는 LimitPI 장애            [Description("Drum1 모터가 회전하지 않거나 LimitPI 신호가 없습니다. (Limit-PI: 드럼 내 필름의 끝을 감지하는 데 사용되는 포토 인터럽터)")]
            | E        | RMS_00054  errorString: Drum1 Motor 또는 LimitPI 장애            [Description("Drum2 모터가 회전하지 않거나 LimitPI 신호가 없습니다. (Limit-PI: 드럼 내 필름의 끝을 감지하는 데 사용되는 포토 인터럽터)")]
            | E        | RMS_00055  errorString: Drum1 Motor 또는 LimitPI 장애            [Description("Drum3 모터가 회전하지 않거나 LimitPI 신호가 없습니다. (Limit-PI: 드럼 내 필름의 끝을 감지하는 데 사용되는 포토 인터럽터)")]
            | E        | RMS_00056  errorString: Drum1 Motor 또는 LimitPI 장애            [Description("Drum4 모터가 회전하지 않거나 LimitPI 신호가 없습니다. (Limit-PI: 드럼 내 필름의 끝을 감지하는 데 사용되는 포토 인터럽터)")]
            | E        | RMS_00100  errorString: 지폐 이송 중 장애 (Banknote Trans Fail)  [Description("지폐 이동에 문제가 있습니다.")]
            | E        | RMS_00102  errorString: 지폐 이송 중 장애                        [Description("잘못된 스태커 오류. 특정 시간 및 엔코더 펄스 수 내에 지폐가 목적지에 도착하지 않습니다. 경로에 있는 전환기, 솔레노이드, IR 센서 및 지폐 이동을 방해하는 장애물을 확인하십시오.")]
            | E        | RMS_00105  errorString: 다크체인 오류(JAM장애)                   [Description("다크체인 오류. JAM입니다. 지폐가 일정 시간 이상 센서 위에 머물렀습니다. JAM을 제거하거나 경로에 있는 IR 센서를 확인하십시오.")]
            | E        | RMS_00106  errorString: 지폐 이송 중 장애(JAM장애)               [Description("지정된 시간과 엔코더 펄스 수 내에 다음 센서에서 지폐가 감지되지 않습니다. JAM을 제거하거나 경로에 있는 IR 센서를 확인하십시오.")]
            | E        | RMS_00107  errorString: 지폐 투입 장애                           [Description("피더 모듈이 지폐를 제대로 피딩할 수 없습니다. 피더 모듈의 유격을 확인하고, 이송을 방해하는 장애물을 제거한 후, 모터의 회전을 확인하시기 바랍니다.")]
------------+----------+----------------------------------------------------------------------
RECYCLER    | E        | RCL_00019  [Description("현재 설정된 Currency 가 아닌 다른 Currency 를 투입했음")]
            | E        | RCL_00026  [Description("Sensor Data 를 취득하지 못하였거나, 시간 내에 취득하지 못함")]
            | E        | RCL_00029  [Description("지폐 인식을 위한 비교 패턴이 없음")]
            | E        | RCL_00030  [Description("지폐 사이즈가 적절하지 못함")]
            | E        | RCL_00031  [Description("권종인식 실패")]
            | E        | RCL_00032  [Description("지폐 연속 투입 시, 첫 번째 장에 인식처리 시간이 긴경우, 다음 장 인식 처리시간이 부족하여 발행하는 에러")]
            | E        | RCL_00033  [Description("표준매체 투입 시, 설정한 면으로 들어가지 않은 경우")]
            | E        | RCL_00035  [Description("드럼이 가득 차거나, 입금된 지폐의 권종이 드럼에 할당이 안되어 지폐가 리젝됨. 또는 지정한 입금 금액이 Over 되서 리젝됨")]
            | E        | RCL_00036  [Description("권종 인식 실패")]
            | E        | RCL_00037  [Description("투입 이상")]
            | E        | RCL_00038  [Description("잘못된 인식 패턴 데이터")]
            | E        | RCL_00041  [Description("MNY 파일이 없음")]
            | E        | RCL_00042  [Description("잘못된 MNY 파일")]
            | E        | RCL_00043  [Description("SVM 파일이 없음")]
            | E        | RCL_00044  [Description("잘못된 SVM 파일")]
            | E        | RCL_00045  [Description("RP 파일이 없음")]
            | E        | RCL_00046  [Description("잘못된 RP 환경파일")]
            | E        | RCL_00047  [Description("RPC 환경파일 없음")]
            | E        | RCL_00048  [Description("잘못된 RPC 환경파일")]
            | E        | RCL_00049  [Description("지폐 투입 이상으로 인한 Jam 발생")]
            | E        | RCL_00054  [Description("지폐가 많이 기울어져 투입됨")]
            | E        | RCL_00055  [Description("Main 이미지의 지폐 네 면의 라인 비대칭")]            
            | E        | RCL_00056  [Description("Sub 이미지의 지폐 네 면의 라인 비대칭")]
            | E        | RCL_00057  [Description("Main 이미지 전처리 시, 지폐 경계 후보점들이 일직선이 아닌 경우")]
            | E        | RCL_00064  [Description("Sub 이미지 전처리 시, 지폐 경계 후보점들이 일직선이 아닌 경우")]
            | E        | RCL_00065  [Description("Main 이미지 지폐 경계 검출에 실패한 경우")]
            | E        | RCL_00066  [Description("Sub 이미지 지폐 경계 검출에 실패한 경우")]
            | E        | RCL_00067  [Description("Main 이미지 전처리 시, 지폐 경계 후보점의 개수가 적은 경우")]
            | E        | RCL_00068  [Description("Sub 이미지 전처리 시, 지폐 경계 후보점의 개수가 적은 경우")]
            | E        | RCL_00069  [Description("지폐 위쪽 영역의 라인을 잘못 찾은경우")]
            | E        | RCL_00070  [Description("지폐 아래쪽 라인을 잘못찾은 경우")]
            | E        | RCL_00071  [Description("지폐 왼쪽 라인을 잘못 찾은경우")]
            | E        | RCL_00072  [Description("지폐 오른쪽 라인을 잘못찾은 경우")]
            | E        | RCL_00073  [Description("투입된 지폐의 위치가 Center 에서 일정 범위를 벗어난 경우")]
            | E        | RCL_00079  [Description("지폐가 여러장 겹쳐서 투입됨")]
            | E        | RCL_00080  [Description("IR 이미지로 지폐 겹침이 검출됨")]
            | E        | RCL_00081  [Description("US 신호 전처리 에러")]
            | E        | RCL_00082  [Description("UV 신호 전처리 에러")]
            | E        | RCL_00083  [Description("MG 신호 전처리 에러")]
            | E        | RCL_00085  [Description("지폐 인식 실패")]
            | E        | RCL_00087  [Description("투입된 지폐가 이미지 센서를 벗어난 경우")]
            | E        | RCL_00089  [Description("Mix Currency 모드 동작 시, 매칭되는 권종의 사이즈가 없는 경우")]
            | E        | RCL_00096  [Description("바코드 인식 실패")]
            | E        | RCL_00097  [Description("잘못된 바코드 에러")]
            | E        | RCL_00098  [Description("바코드 바의 Start 부분과 End 영역의 패턴이 불일치하는 경우")]
            | E        | RCL_00099  [Description("바코드 패턴이 불일치하는 경우")]
            | E        | RCL_00100  [Description("바코드 바 개수 실패")]
            | E        | RCL_00101  [Description("바코드의 노이즈가 너무 많은 경우")]
            | E        | RCL_00103  [Description("지폐의 프린팅 된 부분이 흐려짐")]
            | E        | RCL_00104  [Description("지폐에 낙서가 되어 있는 경우")]
            | E        | RCL_00105  [Description("지폐의 홀로그램 요소가 흐려짐")]
            | E        | RCL_00112  [Description("세탁으로 인한 UV 형광 반응이 생긴 경우")]
            | E        | RCL_00113  [Description("지폐 귀퉁이가 잘린 파손권")]
            | E        | RCL_00114  [Description("지폐 경계 라인이 찢긴 파손권")]
            | E        | RCL_00115  [Description("지폐에 구멍난 파손권")]
            | E        | RCL_00116  [Description("지폐 귀퉁이가 접힌 파손권")]
            | E        | RCL_00117  [Description("지폐 내 Oil 성분으로 오염된 파손권")]
            | E        | RCL_00120  [Description("절체 시간 내에 인식 결과가 전달 되지 않은 경우")]
            | E        | RCL_00121  [Description("인식 Banknote ID 와 SC Banknote ID 가 다름")]
            | E        | RCL_00123  [Description("지폐 간격이 좁음")]
            | E        | RCL_00148  [Description("인식하려는 바코드 영역에 노이즈가 많은 경우")]
            | E        | RCL_00149  [Description("시리얼 인식하려는 문자의 크기가 큰 경우")]
            | E        | RCL_00150  [Description("인식하려는 문자의 문자 외에 노이즈가 많은 경우")]
            | E        | RCL_00151  [Description("시리얼 비교 시, 미스매치 개수가 많은 경우")]
            | E        | RCL_00152  [Description("블랙리스트로 검출된 시리얼")]
            | E        | RCL_00160  [Description("지폐가 2 장 겹칠 때, IR 투과 Double")]
            | E        | RCL_00161  [Description("지폐가 2 장 겹칠 때, VLT Double (입금기에 VLT 이미지 없음 )")]
            | E        | RCL_00162  [Description("DSP 에서 투입된 이미지가 2 장일 때, Insert Chain 으로 발행")]
            | E        | RCL_00163  [Description("Unfit 상태의 Breakage 권")]
            | E        | RCL_00164  [Description("Main 이미지와 Sub 이미지의 사이즈가 차이가 발생할 때")]
            | E        | RCL_00165  [Description("시리얼 영역 전처리 실패")]
            | E        | RCL_00166  [Description("시리얼 영역이 너무 크거나 0 보다 작을 때, 발생")]
            | E        | RCL_00167  [Description("인식하려는 문자의 문자 외에 노이즈가 많은 경우")]
            | E        | RCL_00168  [Description("시리얼 관련 모델 로드 실패")]
            | E        | RCL_00169  [Description("잘못된 시리얼 영역 추출 함수 에러")]
            | E        | RCL_00170  [Description("세로 시리얼 Rotation 실패")]
            | E        | RCL_00171  [Description("시리얼 문자의 매칭되는 SVM 패턴이 없는 경우")]
            | E        | RCL_00193  [Description("IR 반응이 정상권과 달라 위폐로 배출이 된 경우")]
            | E        | RCL_00198  [Description("UV 반응이 정상권과 달라 위폐로 배출된 경우")]
            | E        | RCL_00199  [Description("IR, UV 반응이 정상권과 달라 위폐로 배출이 된 경우")]
            | E        | RCL_00208  [Description("MG 반응이 정상권과 달라 위폐로 배출이 된 경우")]
            | E        | RCL_00209  [Description("IR, MG 반응이 정상권과 달라 위폐로 배출이 된 경우")]
            | E        | RCL_00214  [Description("UV, MG 반응이 정상권과 달라 위폐로 배출이 된 경우")]
            | E        | RCL_00215  [Description("IR, UV, MG 반응이 정상권과 달라 위폐로 배출이 된 경우")]
            | E        | RCL_00224  [Description("인식된 두 개의 Serial 번호가 다름")]
            | E        | RCL_00232  [Description("인식 처리에 필요한 환경 파일(NNP, MNY, SVM 등) 또는 센서 데이터가 없는 경우")]
------------+----------+----------------------------------------------------------------------
SHUTTER     | E        | SRS_00001  통신 장애(시간 초과 또는 포트 이상)
            | E        | SRS_00010  로그 생성 장애
            | E        | SRS_00011  현금/상품권 입금 셔터 열기 시간 초과(5 초)
            | E        | SRS_00012  현금/상품권 입금 셔터 닫기 시간 초과(5초)
            | E        | SRS_00013  현금/상품권 입금 셔터 열기 중 걸림(3회 재시도 후 반환 코드)
            | E        | SRS_00014  현금/상품권 입금 셔터 닫기 중 걸림(3회 재시도 후 반환 코드)
            | E        | SRS_00015  현금 출금 셔터 열기 시간 초과(5초)
            | E        | SRS_00016  현금 출금 셔터 닫기 시간 초과(5초)
            | E        | SRS_00017  현금 출금 셔터 열기 중 걸림(3회 재시도 후 반환 코드)
            | E        | SRS_00018  현금 출금 셔터 닫기 중 걸림(3회 재시도 후 반환 코드)
            | E        | SRS_00019  출금 셔터 닫기 중 손 감지
------------+----------+----------------------------------------------------------------------
GIFTOUT     | E        | GTN_00001  연결 실패
            | E        | GTN_00002  이미 연결되어 있음
            | E        | GTN_00003  타임아웃
            | E        | GTN_00004  데이터 길이 오류 (길이 = 0)
            | E        | GTN_00005  MI 에러
            | E        | GTN_00006  CRC 에러
            | E        | GTN_00007  MI & CRC 에러
            | E        | GTN_00008  비정상 입력 데이터
            | E        | GTN_00009  에러
            | E        | GTN_00010  연결되어 있지 않음
            | E        | GTN_00011  연결 해제 실패
            | E        | GTN_00012  이미 연결 해제 되어 있음
            | E        | GTN_00013  처리중
            | E        | GTN_00014  변환 포트 실패(펌웨어 업그레이드 사용)
            | E        | GTN_00015  경로가 존재하지 않음
            | E        | GTN_00016  경로명 길이 초과 (260 보다 큼)
------------+----------+----------------------------------------------------------------------
GIFTOUT     | E        | GUT_00001  기울어진 지폐 (1)
            | E        | GUT_00002  0x02  짧은 GAP 지폐 (2)
            | E        | GUT_00004  0x04  긴 지폐 (4)
            | E        | GUT_00008  0x08  짧은 지폐 (8)
            | E        | GUT_00016  0x10  중복 방출 (16)
            | E        | GUT_00032  0x20  잘못된 지폐 (32)
------------+----------+----------------------------------------------------------------------
GIFTOUT     | E        | GRT_00001  0x01  Barcode 길이 개수 에러 (1)
            | E        | GRT_00032  0x20  Check Digit 에러 (32)
            | E        | GRT_00047  0x2F  Barcode domain 확인 실패 (47)
            | E        | GRT_00064  0x40  이미지 사이즈 에러 (64)
            | E        | GRT_00128  0x80  바코드 인식 실패 (128)
            | E        | GRT_00255  0xFF  Sequence Number 에러 (255)
------------+----------+----------------------------------------------------------------------
GIFTOUT     | E        | GSP_4000A    통신오류 - ACK/NACK 미수신
            | E        | GSP_4000B    통신오류 - 명령 데이터 포맷 에러 
            | E        | GSP_4000C    통신오류 - DIRECTION 명령 Timeout
            | E        | GSP_4000D    통신오류 - DIRECTION 명령 SEQ 오류
            | E        | GSP_40010    기기오류 - 피드 모터 인코더 오류
            | E        | GSP_40011    CIS 커버 열림
            | E        | GSP_40012    리젝트 박스 잠금 해제
            | E        | GSP_40013    게이트 배출 방식 오류
            | E        | GSP_40014    게이트 주파수 방식 오류
            | E        | GSP_40015    셔터 오픈 에러
            | E        | GSP_40016    셔터 닫기 에러
            | E        | GSP_40017    셔터 센서 오류
            | E        | GSP_40018    방출기 리프트 업 에러
            | E        | GSP_40019    방출기 리프트 다운 에러
            | E        | GSP_4001F    방출기 리프트 업& 다운 에러
            | E        | GSP_4001A    미발출 및 과다 방출 에러 - 연속Reject 매수 Error
            | E        | GSP_4001B    미발출 및 과다 방출 에러 - 총 Reject 매수 에러
            | E        | GSP_4001C    미발출 및 과다 방출 에러 - Reject 매수 OVER 에러
            | E        | GSP_4001D    미발출 및 과다 방출 에러 - 지폐 없음
            | E        | GSP_4001E    미발출 및 과다 방출 에러 - 지폐 PICK UP 타임 아웃 ( PRESENT )
            | E        | GSP_40020    인식부 에러(이미지부) - 이미지부 세팅 에러
            | E        | GSP_40021    인식부 에러(이미지부) - 이미지부 응답 없음
            | E        | GSP_40022    인식부 에러(이미지부) - 이미지부 응답 단계 에러
            | E        | GSP_40023    인식부 에러(이미지부) - 이미지부 응답 BCC 에러
            | E        | GSP_40024    인식부 에러(이미지부) - 이미지부 CIS 보정 실패
            | E        | GSP_40025    인식부 에러(이미지부) - 이미지부 세팅 에러
            | E        | GSP_40026    인식부 에러(이미지부) - 이미지부 응답 타임아웃
            | E        | GSP_40027    인식부 에러(이미지부) - 이미지부 응답 포맷에러
            | E        | GSP_40030    지폐 걸림 장애 - Scan 시작 센서 지폐 감지 
            | E        | GSP_40031    지폐 걸림 장애 - Gate1/2 센서 지폐 감지
            | E        | GSP_40032    지폐 걸림 장애 - Exit 센서 지폐 감지
            | E        | GSP_40033    지폐 걸림 장애 - Reject 센서 지폐 감지
            | E        | GSP_40034    지폐 걸림 장애 - Cassette1 Skew1/2 센서 지폐 감지
            | E        | GSP_40035    지폐 걸림 장애 - Cassette2 Skew1/2 센서 지폐 감지
            | E        | GSP_40036    지폐 걸림 장애 - Cassette3 Skew1/2 센서 지폐 감지
            | E        | GSP_40037    지폐 걸림 장애 - Cassette4 Skew1/2 센서 지폐 감지
            | E        | GSP_40038    지폐 걸림 장애 - Cassette5 Skew1/2 센서 지폐 감지
            | E        | GSP_40039    지폐 걸림 장애 - Cassette6 Skew1/2 센서 지폐 감지
            | E        | GSP_4003F    지폐 걸림 장애 - ESCROW_COUNT1/2 센서 지폐 감지
            | E        | GSP_40040    센세에 지폐 미 도착 - Scan 시작 센서에 지폐 미 도착
            | E        | GSP_40041    센세에 지폐 미 도착 - Gate1/2  센서에 지폐 미 도착
            | E        | GSP_40042    센세에 지폐 미 도착 - Exit1/2 센서에 지폐 미 도착
            | E        | GSP_40043    센세에 지폐 미 도착 - Reject 센서에 지폐 미 도착
            | E        | GSP_4004F    센세에 지폐 미 도착 - Escrow_count1/2 센서에 지폐 미 도착
            | E        | GSP_40050    비정상적 매체 - Scan 시작 센서에 비정상 지폐 감지
            | E        | GSP_40051    비정상적 매체 - Gate1/2  센서에 비정상 지폐 감지
            | E        | GSP_40052    비정상적 매체 - Exit1/2 센서에 비정상 지폐 감지
            | E        | GSP_40053    비정상적 매체 - Reject 센서에 비정상 지폐 감지
            | E        | GSP_4005F    비정상적 매체 - Escrow_count1/2 센서에 비정상 지폐 감지
            | E        | GSP_40060    이송부 센서 에러 - Scan 시작 센서 지폐 감지
            | E        | GSP_40061    이송부 센서 에러 - Gate1 센서 지폐 감지
            | E        | GSP_40062    이송부 센서 에러 - Gate2 센서 지폐 감지
            | E        | GSP_40063    이송부 센서 에러 - Exit1 센서 지폐 감지
            | E        | GSP_40064    이송부 센서 에러 - Reject 센서 지폐 감지
            | E        | GSP_40065    이송부 센서 에러 - Escrow 센서(shut_in1) 센서 지폐 감지
            | E        | GSP_40066    이송부 센서 에러 - Escrow 센서(shut_in2) 센서 지폐 감지
            | E        | GSP_40067    이송부 센서 에러 - Escrow 센서(shut_in3) 센서 지폐 감지
            | E        | GSP_40068    이송부 센서 에러 - Escrow Count1 센서 지폐 감지
            | E        | GSP_40069    이송부 센서 에러 - Escrow Count2 센서 지폐 감지
            | E        | GSP_4006A    이송부 센서 에러 - Retract_Reject 센서 지폐 감지
            | E        | GSP_4006B    이송부 센서 에러 - Escrow Exist 센서 지폐 감지
            | E        | GSP_40070    카세트 센서 오류 - Cassette1 Skew1 센서 지폐 감지
            | E        | GSP_40070    카세트 센서 오류 - Cassette2 Skew1 센서 지폐 감지
            | E        | GSP_40070    카세트 센서 오류 - Cassette3 Skew1 센서 지폐 감지
            | E        | GSP_40070    카세트 센서 오류 - Cassette4 Skew1 센서 지폐 감지
            | E        | GSP_40070    카세트 센서 오류 - Cassette5 Skew1 센서 지폐 감지
            | E        | GSP_40070    카세트 센서 오류 - Cassette6 Skew1 센서 지폐 감지
            | E        | GSP_40070    카세트 센서 오류 - Cassette1 Skew2 센서 지폐 감지
            | E        | GSP_40070    카세트 센서 오류 - Cassette2 Skew2 센서 지폐 감지
            | E        | GSP_40070    카세트 센서 오류 - Cassette3 Skew2 센서 지폐 감지
            | E        | GSP_40070    카세트 센서 오류 - Cassette4 Skew2 센서 지폐 감지
            | E        | GSP_4007A    카세트 센서 오류 - Cassette5 Skew2 센서 지폐 감지
            | E        | GSP_4007B    카세트 센서 오류 - Cassette6 Skew2 센서 지폐 감지
            | E        | GSP_40080    방출중 PICK UP 장애 - 1번 카세트 PICK UP장애(지폐 있음)
            | E        | GSP_40081    방출중 PICK UP 장애 - 2번 카세트 PICK UP장애(지폐 있음)
            | E        | GSP_40082    방출중 PICK UP 장애 - 3번 카세트 PICK UP장애(지폐 있음)
            | E        | GSP_40083    방출중 PICK UP 장애 - 4번 카세트 PICK UP장애(지폐 있음)
            | E        | GSP_40084    방출중 PICK UP 장애 - 5번 카세트 PICK UP장애(지폐 있음)
            | E        | GSP_40085    방출중 PICK UP 장애 - 6번 카세트 PICK UP장애(지폐 있음)
            | E        | GSP_40088    방출중 PICK UP 장애 - 1번 카세트 PICK UP장애(지폐 없음)
            | E        | GSP_40089    방출중 PICK UP 장애 - 2번 카세트 PICK UP장애(지폐 없음)
            | E        | GSP_4008A    방출중 PICK UP 장애 - 3번 카세트 PICK UP장애(지폐 없음)
            | E        | GSP_4008B    방출중 PICK UP 장애 - 4번 카세트 PICK UP장애(지폐 없음)
            | E        | GSP_4008C    방출중 PICK UP 장애 - 5번 카세트 PICK UP장애(지폐 없음)
            | E        | GSP_4008D    방출중 PICK UP 장애 - 6번 카세트 PICK UP장애(지폐 없음)
            | E        | GSP_40090    카세트 관련 장애 - 1번 카세트 없음
            | E        | GSP_40091    카세트 관련 장애 - 2번 카세트 없음
            | E        | GSP_40092    카세트 관련 장애 - 3번 카세트 없음
            | E        | GSP_40093    카세트 관련 장애 - 4번 카세트 없음
            | E        | GSP_40094    카세트 관련 장애 - 5번 카세트 없음
            | E        | GSP_40095    카세트 관련 장애 - 6번 카세트 없음
------------+----------+----------------------------------------------------------------------
BTOUT       | E        | BTN_00001  COM 포트 장애 (시간 초과 또는 포트 이상)
            | E        | BTN_00010  로그 생성 장애
            | E        | BTN_00013  롤러 부분으로 픽업 장애 (3회 재 시도 후)
            | E        | BTN_00014  지급 중 진입부 걸림 장애
            | E        | BTN_00015  지급 중 출구부 걸림 장애
            | E        | BTN_00016  봉투 적재량 없음
------------+----------+----------------------------------------------------------------------
IOCNTR      | E        | ITN_00001  통신 장애 (시간 초과 또는 포트 이상)
            | E        | ITN_00010  로그 생성 장애
            | I        | ITN10001  도어락 잠금 해제
            | I        | ITN10002  도어락 잠금
------------+----------+----------------------------------------------------------------------
"""

# 데이터 행을 줄바꿈 기준으로 분리
lines = data.split('\n')

# 데이터를 저장할 리스트 초기화
parsed_data = []

# 정규 표현식을 사용하여 각 컬럼을 추출
pattern = r'^\s*(\w+)?\s*\|\s*(\w+)?\s*\|\s*([\w_]+)?\s*-\s*(.+)'

for line in lines:
    match = re.match(pattern, line)
    if match:
        device, error_type, code, description = match.groups()
        parsed_data.append([device, error_type, code, description])

# 데이터프레임으로 변환
df = pd.DataFrame(parsed_data, columns=['디바이스명', '장애구분', '코드', '설명'])

# 디바이스명, 장애구분 값이 없는 행을 이전 행의 값으로 채움
df['디바이스명'].ffill(inplace=True)
df['장애구분'].ffill(inplace=True)

# 결과 확인
print(df)