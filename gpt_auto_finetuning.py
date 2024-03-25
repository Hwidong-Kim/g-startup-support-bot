import json
import os
import time
import re

from openai import OpenAI
from pathlib import Path


save_path = "./auto_data.jsonl"

raw_data = [
    {
        "title": {
            "name": "세상을 밝히는 따뜻한 기술, 에이블테크 스타트업",
            "logo_url": "/comm/viewImage.do?f=3%2BFWnIt61%2Fl%2FGTbAEMaZDWFVlGE3Z15SDEpxTkMEDkJFfiKkSuPftRb5%2BpULN9RW"
        },
        "contents": [
            "함께도약\nK-Startup\n세상을 밝히는 따뜻한 기술\n에이블테크\n사회적 약자 배려 기술\n중소벤처기업부, 창업진흥원",
            "과학기술과 정보통신의 고도화 덕분에 우리는 더욱 다채롭고 풍요로운 삶을 영위하고 있다. 그런데 이러한 혜택을 누리고 이용하는 데에 어려움을 겪는 사회적 약자가 있다. 바로 장애인이다. 보건복지부에 따르면 2022년 기준 등록장애인 수는 265만 2,860명으로, 이는 우리나라 전체 인구의 5%가 넘는 수치이다. 이러한 사회적 문제는 다양한 유형의 장애를 가진 이들을 배려하는 기술인 에이블테크(able-tech)에 대한 관심을 불러 일으켰다.",
            "정부 역시 에이블테크와 관련해 적극적인 모습을 보이고 있다. 정부는 지난 8일 점자 정책 기본 방향을 제시하며, 점자 사용자가 공정하게 정보에 접근할 수 있도록 점자 교육의 확대와 점자 발전 기반 강화를 목표로 정했다. 시각 보조를 위한 점자의 지속적 발전을 위해 정책 기반을 강화하고 맞춤형 점자 교육을 통해 점자 사용 능력을 향상시킨다는 계획이다.",
            "특히 눈여겨봐야할 부분은 올해부터 점자 교원 자격제도와 점자 능력 검정 제도의 도입을 위한 연구, 시행령 개정, 제도 도입 및 운영 등을 순차적으로 추진한다는 점이다. 또한 2028년까지 1,350만 어절의 묵자-점자 말뭉치를 구축해 인공지능을 활용한 자동 점역 기술 개발을 지원할 계획이라는 점도 눈길을 끈다. 이렇게 점자 교육의 중요성이 대두되는 가운데 이와 관련한 기술부터 다양한 유형의 장애를 가진 이들을 위한 서비스를 개발한 에이블테크 스타트업을 알아본다.",
            "<센시>\n‘센시’는 시각장애인을 대상으로 점자 변환 서비스를 제공하는 기업이다. 인공지능을 기반으로 서적의 글자, 이미지를 비롯한 복잡한 수식도 점자로 변환해 주는 알고리즘을 구현했다. 보통 300페이지 분량의 점자책을 제작하는 데 6개월 정도가 소요되나, 센시의 솔루션을 활용하면 하루만에도 제작이 가능하다. 이 기술은 점자책 제작 비용을 기존방식 대비 10분의 1 수준으로 절감하는 등 비용 효율성을 극대화한다. 이처럼 센시는 시각장애인이 합리적 비용으로 다양한 콘텐츠를 쉽게 경험할 수 있도록 정보 접근성을 높이고 있다.",
            "<오파테크>\n‘오파테크’는 시각장애인이 점자를 쉽고 재미있게 배울 수 있도록 세계 최초의 점자 학습기 '탭틸로'를 개발했다. 건반악기인 멜로디언과 비슷한 생김새의 탭틸로는 점자 모양을 만질 수 있는 디스플레이와 점자를 쓸 수 있는 블록으로 구성돼 있다. 사용자는 디스플레이에 올라온 점자 모양을 만져 점자를 읽고, 블록을 이용해 점자를 눌러 쓰는 법을 익힐 수 있다. 오파테크는 국내뿐만 아니라 인도네시아 학교에도 학습기를 보급하는 등 시각장애인의 점자 문맹률을 낮추기 위해 글로벌 시장을 개척하고 있다.",
            "<소보로>\n‘소보로’는 ‘소리를 보는 통로’의 줄임말로 청각장애인의 소통 편의을 돕는 IT기업이다. 실시간으로 인식한 소리를 문자로 변환하는 서비스를 제공하고 있으며, 이를 통해 청각장애인은 의사소통 도우미가 없는 환경에서도 강연이나 회의 등에 참여할 수 있다. 또한 대량의 음성파일을 녹취록이나 텍스트 파일로 변환해 주는 서비스를 선보이는 등 장애인들이 겪고 있는 불편을 해결하기 위해 다양한 솔루션을 개발하고 있다. 소보로는 향후 청각뿐만 아니라 다른 유형의 장애인을 위한 전용 서비스를 늘려나갈 계획이다.",
            "<셀리코>\n‘셀리코’는 전자장치를 통해 앞을 보게 해주는 의료기기인 ‘전자눈’을 개발하고 있다. 증강현실(AR) 스마트 글래스에 탑재된 고해상도 카메라를 통해 촬영된 이미지를 영상처리하여 보이지 않는 부분을 시각화한다. 아직 시력 손상이 심하지 않은 초·중기 환자들은 이를 시력 보조장치로 쓸 수 있으며, 빅데이터 기반의 시야 검사 프로그램을 통해 집에서 간편하게 시력 측정을 할 수 있다. 이를 통해 셀리코는 CES 2024 혁신상 수상에 이어 에디슨 어워드 최종 후보자에 오르는 등 전자눈 시장에서 두각을 드러내고 있다.",
            "<와들>\n‘와들’은 시각장애인을 위한 AI 기반 모바일 쇼핑 플랫폼 ‘소리마켓’을 운영하는 기업이다. 시각장애인은 스마트폰의 텍스트를 읽어주는 스크린리더를 활용해 정보와 내용을 인지할 수 있다. 하지만 다수의 온라인 쇼핑몰이 상품의 텍스트 기반 정보를 이미지로 업로드 하기 때문에 스크린리더가 텍스트를 인식할 수 없게 된다. 이러한 불편을 해결하기 위해 이미지 내에 포함된 텍스트를 추출해 음성으로 정보를 변환해 주는 서비스를 운영하고 있다. 와들은 대화형 AI 기술도 개발해 시각장애인뿐만 아니라 노년층과 같은 정보 취약 계층의 정보접근성 향상을 위해 노력하고 있다. ",
            "<시공간>\n‘시공간’은 시각장애인의 정보 접근성 향상을 위해 다양한 플랫폼을 개발하고 있다. 시각장애인의 온라인 쇼핑을 돕는 ‘픽포미’는 AI와 사람이 상품을 분석 및 추천하여 쇼핑의 어려움을 해소한다. 또한 시각장애인이 인식할 수 없는 사진, 그림에 대한 설명을 제공하는 ‘글공방’, 시각장애인과 비장애인 도우미를 연결하는 ‘봄자국’ 등을 운영하고 있다. 시공간은 이처럼 누구나 정보에 쉽게 접근할 수 있는 디지털 환경을 조성하기 위해 매진하고 있다. ",
            "<브이드림>\n‘브이드림’은 기업과 장애인 근로자의 업무 소통을 돕기 위해 재택근무 관리 시스템 ‘플립’을 운영하고 있다. 구직 중인 장애인과 기업을 매칭하고, 플립을 통해 출결 관리, 회의 참여 및 업무요청 등을 해결할 수 있도록 서비스를 제공한다. 음성인식 및 실시간 자막 기능도 탑재해 웹 접근성을 강화했으며, 이를 통해 장애인이 재택근무 중에도 원활한 업무 소통을 할 수 있도록 돕는다. 브이드림은 디지털 혁신을 통해 장애인의 사회 진출을 돕고 있으며, 누구나 제약 없이 일할 수 있는 근무 환경을 지향하고 있다.",
            "<엘비에스테크>\n‘엘비에스테크’는 장애인 및 교통약자의 보행·이동권 증진을 위해 스마트 시티 플랫폼을 구축하고 있다. ‘지아이플러스’는 시각 장애인이 목적지로 이동할 때 필요한 각종 지형, 공간, 기상 등과 같은 정보를 소리와 진동으로 알리며 길잡이 역할을 한다. 또한 휠체어 이용자들을 위해 건물 내 진입 가능 여부와 통과할 수 있는 문 등의 정보도 제공한다. 카페나 식당 등에서 주문 및 결제를 돕는 음성 서비스 기능도 탑재해 장애인의 도시 접근성을 높이고 있다. 엘비에스테크는 최근 영국 런던에서 솔루션 실증을 추진하는 등 유럽 진출에도 박차를 가하고 있다.   ",
            "<캥스터즈>\n‘캥스터즈’는 휠체어 사용자들이 본인의 휠체어로 유산소 운동을 즐길 수 있는 솔루션인 ‘휠리엑스’ 운영하고 있다. 이용자는 휠체어를 타고 러닝머신 위에 올라가 롤러를 굴리며 운동할 수 있으며, 언제 어디서나 체력을 증진시킬 수 있다는 장점이 있다. 전용 앱에 트레이닝 모드, 게임 등의 다양한 운동 콘텐츠를 결합해 흥미를 이끌어내고, 장애의 유형 및 정도를 고려해 개인 맞춤형 운동 콘텐츠도 제공하고 있다. 지난해 전국장애인e스포츠대회의 정식 종목으로 휠리엑스가 채택되는 등 캥스터즈는 누구나 제약 없이 체육활동을 즐길 수 있도록 시장을 선도하고 있다.",
            "앞서 살펴본 에이블테크의 영역은 점자를 이용해 시각 보조를 하는 서비스부터 이동·청력·근력보조 등 장애인과 사회적 약자의 삶의 질을 개선하는 등 그 범위가 광범위하다. 장애인을 비롯한 사회적 약자들도 차별과 제약 없이 사회 구성원으로서 그 역할을 수행하는데 도움을 줄 수 있는 에이블테크 및 서비스들이 지속적으로 개발되고 있다. 만물이 깨어나고 태동하는 계절이 성큼 다가온 요즘, 봄볕만큼이나 따뜻한 기술을 통해 즐거움과 편리함을 모두가 함께 누리며 살 수 있는 밝은 미래가 다가오길 기대해 본다.",
            "중소벤처기업부, 창업진흥원",
            "함께도약\nK-Startup\n세상을 밝히는 따뜻한 기술\n에이블테크\n사회적 약자 배려 기술\n중소벤처기업부, 창업진흥원",
            "과학기술과 정보통신의 고도화 덕분에 우리는 더욱 다채롭고 풍요로운 삶을 영위하고 있다. 그런데 이러한 혜택을 누리고 이용하는 데에 어려움을 겪는 사회적 약자가 있다. 바로 장애인이다. 보건복지부에 따르면 2022년 기준 등록장애인 수는 265만 2,860명으로, 이는 우리나라 전체 인구의 5%가 넘는 수치이다. 이러한 사회적 문제는 다양한 유형의 장애를 가진 이들을 배려하는 기술인 에이블테크(able-tech)에 대한 관심을 불러 일으켰다.",
            "정부 역시 에이블테크와 관련해 적극적인 모습을 보이고 있다. 정부는 지난 8일 점자 정책 기본 방향을 제시하며, 점자 사용자가 공정하게 정보에 접근할 수 있도록 점자 교육의 확대와 점자 발전 기반 강화를 목표로 정했다. 시각 보조를 위한 점자의 지속적 발전을 위해 정책 기반을 강화하고 맞춤형 점자 교육을 통해 점자 사용 능력을 향상시킨다는 계획이다.",
            "특히 눈여겨봐야할 부분은 올해부터 점자 교원 자격제도와 점자 능력 검정 제도의 도입을 위한 연구, 시행령 개정, 제도 도입 및 운영 등을 순차적으로 추진한다는 점이다. 또한 2028년까지 1,350만 어절의 묵자-점자 말뭉치를 구축해 인공지능을 활용한 자동 점역 기술 개발을 지원할 계획이라는 점도 눈길을 끈다. 이렇게 점자 교육의 중요성이 대두되는 가운데 이와 관련한 기술부터 다양한 유형의 장애를 가진 이들을 위한 서비스를 개발한 에이블테크 스타트업을 알아본다.",
            "<센시>\n‘센시’는 시각장애인을 대상으로 점자 변환 서비스를 제공하는 기업이다. 인공지능을 기반으로 서적의 글자, 이미지를 비롯한 복잡한 수식도 점자로 변환해 주는 알고리즘을 구현했다. 보통 300페이지 분량의 점자책을 제작하는 데 6개월 정도가 소요되나, 센시의 솔루션을 활용하면 하루만에도 제작이 가능하다. 이 기술은 점자책 제작 비용을 기존방식 대비 10분의 1 수준으로 절감하는 등 비용 효율성을 극대화한다. 이처럼 센시는 시각장애인이 합리적 비용으로 다양한 콘텐츠를 쉽게 경험할 수 있도록 정보 접근성을 높이고 있다.",
            "<오파테크>\n‘오파테크’는 시각장애인이 점자를 쉽고 재미있게 배울 수 있도록 세계 최초의 점자 학습기 '탭틸로'를 개발했다. 건반악기인 멜로디언과 비슷한 생김새의 탭틸로는 점자 모양을 만질 수 있는 디스플레이와 점자를 쓸 수 있는 블록으로 구성돼 있다. 사용자는 디스플레이에 올라온 점자 모양을 만져 점자를 읽고, 블록을 이용해 점자를 눌러 쓰는 법을 익힐 수 있다. 오파테크는 국내뿐만 아니라 인도네시아 학교에도 학습기를 보급하는 등 시각장애인의 점자 문맹률을 낮추기 위해 글로벌 시장을 개척하고 있다.",
            "<소보로>\n‘소보로’는 ‘소리를 보는 통로’의 줄임말로 청각장애인의 소통 편의을 돕는 IT기업이다. 실시간으로 인식한 소리를 문자로 변환하는 서비스를 제공하고 있으며, 이를 통해 청각장애인은 의사소통 도우미가 없는 환경에서도 강연이나 회의 등에 참여할 수 있다. 또한 대량의 음성파일을 녹취록이나 텍스트 파일로 변환해 주는 서비스를 선보이는 등 장애인들이 겪고 있는 불편을 해결하기 위해 다양한 솔루션을 개발하고 있다. 소보로는 향후 청각뿐만 아니라 다른 유형의 장애인을 위한 전용 서비스를 늘려나갈 계획이다.",
            "<셀리코>\n‘셀리코’는 전자장치를 통해 앞을 보게 해주는 의료기기인 ‘전자눈’을 개발하고 있다. 증강현실(AR) 스마트 글래스에 탑재된 고해상도 카메라를 통해 촬영된 이미지를 영상처리하여 보이지 않는 부분을 시각화한다. 아직 시력 손상이 심하지 않은 초·중기 환자들은 이를 시력 보조장치로 쓸 수 있으며, 빅데이터 기반의 시야 검사 프로그램을 통해 집에서 간편하게 시력 측정을 할 수 있다. 이를 통해 셀리코는 CES 2024 혁신상 수상에 이어 에디슨 어워드 최종 후보자에 오르는 등 전자눈 시장에서 두각을 드러내고 있다.",
            "<와들>\n‘와들’은 시각장애인을 위한 AI 기반 모바일 쇼핑 플랫폼 ‘소리마켓’을 운영하는 기업이다. 시각장애인은 스마트폰의 텍스트를 읽어주는 스크린리더를 활용해 정보와 내용을 인지할 수 있다. 하지만 다수의 온라인 쇼핑몰이 상품의 텍스트 기반 정보를 이미지로 업로드 하기 때문에 스크린리더가 텍스트를 인식할 수 없게 된다. 이러한 불편을 해결하기 위해 이미지 내에 포함된 텍스트를 추출해 음성으로 정보를 변환해 주는 서비스를 운영하고 있다. 와들은 대화형 AI 기술도 개발해 시각장애인뿐만 아니라 노년층과 같은 정보 취약 계층의 정보접근성 향상을 위해 노력하고 있다. ",
            "<시공간>\n‘시공간’은 시각장애인의 정보 접근성 향상을 위해 다양한 플랫폼을 개발하고 있다. 시각장애인의 온라인 쇼핑을 돕는 ‘픽포미’는 AI와 사람이 상품을 분석 및 추천하여 쇼핑의 어려움을 해소한다. 또한 시각장애인이 인식할 수 없는 사진, 그림에 대한 설명을 제공하는 ‘글공방’, 시각장애인과 비장애인 도우미를 연결하는 ‘봄자국’ 등을 운영하고 있다. 시공간은 이처럼 누구나 정보에 쉽게 접근할 수 있는 디지털 환경을 조성하기 위해 매진하고 있다. ",
            "<브이드림>\n‘브이드림’은 기업과 장애인 근로자의 업무 소통을 돕기 위해 재택근무 관리 시스템 ‘플립’을 운영하고 있다. 구직 중인 장애인과 기업을 매칭하고, 플립을 통해 출결 관리, 회의 참여 및 업무요청 등을 해결할 수 있도록 서비스를 제공한다. 음성인식 및 실시간 자막 기능도 탑재해 웹 접근성을 강화했으며, 이를 통해 장애인이 재택근무 중에도 원활한 업무 소통을 할 수 있도록 돕는다. 브이드림은 디지털 혁신을 통해 장애인의 사회 진출을 돕고 있으며, 누구나 제약 없이 일할 수 있는 근무 환경을 지향하고 있다.",
            "<엘비에스테크>\n‘엘비에스테크’는 장애인 및 교통약자의 보행·이동권 증진을 위해 스마트 시티 플랫폼을 구축하고 있다. ‘지아이플러스’는 시각 장애인이 목적지로 이동할 때 필요한 각종 지형, 공간, 기상 등과 같은 정보를 소리와 진동으로 알리며 길잡이 역할을 한다. 또한 휠체어 이용자들을 위해 건물 내 진입 가능 여부와 통과할 수 있는 문 등의 정보도 제공한다. 카페나 식당 등에서 주문 및 결제를 돕는 음성 서비스 기능도 탑재해 장애인의 도시 접근성을 높이고 있다. 엘비에스테크는 최근 영국 런던에서 솔루션 실증을 추진하는 등 유럽 진출에도 박차를 가하고 있다.   ",
            "<캥스터즈>\n‘캥스터즈’는 휠체어 사용자들이 본인의 휠체어로 유산소 운동을 즐길 수 있는 솔루션인 ‘휠리엑스’ 운영하고 있다. 이용자는 휠체어를 타고 러닝머신 위에 올라가 롤러를 굴리며 운동할 수 있으며, 언제 어디서나 체력을 증진시킬 수 있다는 장점이 있다. 전용 앱에 트레이닝 모드, 게임 등의 다양한 운동 콘텐츠를 결합해 흥미를 이끌어내고, 장애의 유형 및 정도를 고려해 개인 맞춤형 운동 콘텐츠도 제공하고 있다. 지난해 전국장애인e스포츠대회의 정식 종목으로 휠리엑스가 채택되는 등 캥스터즈는 누구나 제약 없이 체육활동을 즐길 수 있도록 시장을 선도하고 있다.",
            "앞서 살펴본 에이블테크의 영역은 점자를 이용해 시각 보조를 하는 서비스부터 이동·청력·근력보조 등 장애인과 사회적 약자의 삶의 질을 개선하는 등 그 범위가 광범위하다. 장애인을 비롯한 사회적 약자들도 차별과 제약 없이 사회 구성원으로서 그 역할을 수행하는데 도움을 줄 수 있는 에이블테크 및 서비스들이 지속적으로 개발되고 있다. 만물이 깨어나고 태동하는 계절이 성큼 다가온 요즘, 봄볕만큼이나 따뜻한 기술을 통해 즐거움과 편리함을 모두가 함께 누리며 살 수 있는 밝은 미래가 다가오길 기대해 본다.",
            "중소벤처기업부, 창업진흥원"
        ]
    },
    {
        "title": {
            "name": "미래농업 생태계 구축의 핵심! K-애그테크",
            "logo_url": "/comm/viewImage.do?f=NR25mdB%2F3wOgKh%2BlIpYn4x7DuN8SJ0pq7MvJkdFnThchD4PmxbvSJRnZKftJVaJP"
        },
        "contents": [
            "디지털 핫이슈\n\n\n\nK-STARTUP\n\n\n\n미래농업 생태계 구축의 핵심, K-애그테크\n\n\n\n농업과 첨단기술의 만남\n\n\n\n중소벤처기업부 창업진흥원",
            "최근 저출생과 관련해 다양한 이슈가 논의되고 있는 가운데, 농어촌의 고령화와 소멸 현상 또한 심각한 문제로 떠오르고 있다. 한편, 전 세계적 기후변화로 인한 식량 생산량의 감소에 ‘농업(agriculture)’과 ‘기술(technology)’을 접목한 애그테크(Ag-tech)가 위기 극복의 대안으로 주목받고 있다. 애그테크는 스마트농업의 기반을 이루는 농업 관련 기술의 총칭으로 인공지능(AI)·사물인터넷(IoT)·빅데이터 등 첨단 기술을 농작물의 생산과 유통 전 과정에 적용한 것이다. \n",
            "정부에서도 농업과 농촌의 활성화 및 기후변화 대비 등을 위해 많은 노력을 기울이고 있다. 농작업의 전 과정을 기계화하고, 자율주행 농업로봇 개발을 확대하는 등 첨단 과학기술을 활용한 현장 문제 해결에 나서기로 했다. 또한 식량자급률 제고 등 농업 분야 공공 연구개발(R&D)을 강화하고, 스마트농업 확산과 바이오 융복합 혁신 기술 개발을 통해 미래 신성장 동력 마련에 노력하고 있다. 미래의 식량을 책임질 애그테크의 중요성이 대두되는 가운데 이와 관련해 대한민국 농축산업의 밝은 미래를 이끌어갈 K-애그테크 스타트업을 알아본다.\n",
            "<파미레세>\n‘파미레세’는 AI를 기반으로 디지털 육종을 개발하는 기업이다. 디지털 육종이란 기존 육종의 핵심 과정을 인공지능으로 대체하는 기술을 뜻한다. 현재 파미레세는 딸기·고추 재배 등에 디지털 육종을 적용해 생산성과 효율성을 높이고 있으며, 기존의 육종 방식보다 빠르고 정밀하게 새로운 품종을 개량하고 있다. 또한 스마트팜 뿐만 아니라 다양한 재배 환경에서도 구현 가능한 고기능성 품종을 연구하고 있다. 파미레세는 지속가능한 농업을 위해 디지털 전환을 이루는 등 미래 농업을 선도하고 있다.\n",
            "<지엘아이엔에스>\n‘지엘아이엔에스’는 농기계에 활용되는 제어 모듈을 개발하는 기업이다. 하나의 기기에서 트랙터나 콤바인과 같은 농기계의 주행 및 작업 등을 개별적으로 제어할 수 있는 통합 시스템을 구축하고 있다. 또한 높은 수준의 차량 표준통신규격을 기반으로 신속하게 데이터를 처리할 수 있고, 빛 탐지 및 범위 측정 감지기 등 첨단기술을 활용해 자율주행 농기계로의 확장도 수월하다. 지엘아이엔에스는 농업 완전 자동화라는 목표 아래 대형 농기계 시장이 활성화된 해외 시장에도 진출할 계획이다.\n",
            "<아그모>\n‘아그모’도 농기계 자율주행 모빌리티를 개발하고 있다. 트랙터, 이앙기 등과 같은 기존에 사용하던 농기계에 ‘아그모 솔루션’ 키트를 부착해 자율주행 농기계로 사용할 수 있다. 한 번의 운행으로 경로 및 데이터를 학습해 이후의 작업은 자율주행으로 처리할 수 있으며, 후진, 유턴 등도 가능해 우리나라처럼 다각형의 농지가 많은 아시아 국가에 적합하다. 또한 운행 중에 토양 상태 및 작물 데이터 등을 파악하고 이를 기반으로 분석해 농업 솔루션을 제공한다. 아그모는 운전자가 개입하는 현재의 자율주행 모델에서 더 나아가 완전 무인 자율주행 모델을 목표로 박차를 가하고 있다.\n",
            "<네토그린>\n‘네토그린’은 머신러닝 기반 농업 데이터 플랫폼을 운영하는 기업이다. 전문적인 농업 지식 습득이나 시간 투자 등의 부담 없이 일반인도 안정적으로 운영할 수 있는 스마트팜 솔루션을 제공하고 있으며, 스마트팜 초기 비용을 줄여 진입장벽을 낮추고 있다. 수직 농장을 활용해 공간의 활용성을 높였고, 실내 농장의 장점을 살려 사시사철 재배할 수 있는 시스템을 구축해 수확량 또한 높였다. 농장 시설뿐만 아니라 시스템 및 유통망에 이르기까지 스마트팜 종합 솔루션을 통해 농업 패러다임을 바꾸고 있다.\n",
            "<에이아이에스>\n온실과 달리 노지는 재배 환경을 제어할 수 없기 때문에 수확량 및 생육 상태에 대해 정확히 예측하기 어렵다. 대한민국 토지 중 90% 이상인 노지를 활용해 솔루션을 제공하는 기업이 있다. ‘에이아이에스’는 알고리즘 기반 농작물 재배관리 플랫폼을 통해 노지에서도 작물이 잘 자랄 수 있는 조건 및 정보 서비스를 제공하고 있다. 전 세계의 작물 생육 데이터를 분석하여 햇빛·광합성·토양·수분 등 작물 재배에 적합한 조건을 추천한다. 재해 리스크 관리는 물론 다음 작기와 관련해 보완할 점을 분석하는 등 체계적인 스마트 농업 시스템을 제공하고 있다.\n",
            "<만나씨이에이>\n‘만나씨이에이’는 아쿠아포닉스 기반의 스마트팜을 구축하고 있다. 아쿠아포닉스는 물고기를 양식하는 과정에서 배출되는 암모니아를 활용해 식물 배양액으로 이용하고, 식물이 정화한 물로 다시 물고기를 키우는 방식이다. 토양재배에서 발생하는 박테리아 감염 및 병해충 피해를 줄일 수 있고, 농약 및 합성 물질을 사용하지 않아 유기농·친환경 작물 생산에 적합하다. 만나씨이에이는 최근 AI 로봇 기업 ‘슈어모빌리티’와 협업을 하는 등 스마트팜의 재배 효율성을 높이기 위해 매진하고 있다.\n",
            "<드림팜>\n‘드림팜’은 자동화 청정 재배시설인 '스마트팜 큐브'를 운영하고 있다. ICT를 활용해 제어할 수 있는 큐브형 스마트팜 시설로 농업이 어려운 곳에서도 작물을 재배할 수 있도록 개발했다. 물이 흐르면서도 일정하게 낮은 온도를 유지하거나 습도를 조절할 수 있어 까다로운 생육환경의 작물도 기를 수 있다. 주로 고추냉이, 루콜라, 로메인 등 저온성 작물들을 주력으로 내세우고 있으며, 중동처럼 날씨가 더운 나라에서도 이를 활용해 작물을 재배할 수 있다. 실제로 드림팜은 사우디, 카타르, 베트남 등에 스마트팜 큐브를 수출하는 등 해외 시장에서도 첨단 농업 기술력을 선보이고 있다.\n",
            "<퓨처커넥트>\n‘퓨처커넥트’는 IoT 기반 스마트팜 공급 및 신선채소 판매 플랫폼을 운영하는 기업이다. 도심 속에서도 재배 가능한 모듈형 스마트팜 설계 기술과 더불어 인공지능 기반 자동 재배 기술, 농장 생산망 모니터링 및 제어 등이 핵심 솔루션이다. 이를 기반으로 도심 유휴공간 곳곳에서 작물을 재배하고 실시간 수요량에 따라 공급하는 등 누구나 신선한 채소를 섭취할 수 있도록 서비스를 운영하고 있다. 또한 구축된 농장 생산망을 통해 대규모 사옥, 주거단지, 공유오피스 등에 구독 형태의 모종 배송 서비스를 제공하는 등 다양한 비즈니스 모델을 갖추고 있다.\n",
            "<넥스트온>\n‘넥스트온’은 세계 최초로 IoT 기반 수직형 스마트팜을 통해 딸기를 연중 재배에 성공했다. 자체 LED 기술을 통해 최소한의 전력으로 농작물 광합성에 필요한 광량을 공급하며, 온습도·바람 제어 시스템과 더불어 자동 관개 시스템을 통해 유속 및 유량을 조절해 재배가 까다로운 작물도 재배할 수 있도록 한다. 또한 현대 미술 작가들과 협업을 통해 도심 속 스마트팜과 예술을 결합하여 관광객들의 이목을 끄는 등 단순 농장이 아닌 산업 관광으로서의 성장 가능성도 보여주고 있다. \n",
            "<아이오크롭스>\n‘아이오크롭스’는 인공지능을 기반으로 재배 및 데이터 수집·분석, 경영 관리까지 가능한 농작업 로봇을 개발하고 있다. 온실을 완전 자율 주행하는 로봇을 통해 자동으로 농장의 데이터를 수집할 수 있고, 이를 통해 다양한 온실 작물을 실시간으로 모니터링 하며 생장 상태를 확인할 수 있다. 로봇이 수집한 데이터를 통해 생육 지표를 분석하고, 이를 활용해 과실의 당도, 크기 및 수량 등을 예측할 수 있다. 아이오크롭스는 병해충 탐지 및 수확·운반 등에 이르기까지 완전 무인 자동화 시스템을 구축해 나갈 계획이다.\n",
            "<파이프트리>\n‘파이프트리’는 인공지능을 기반으로 양계농가의 질병 예찰 및 관리 시스템 ‘파머스 마인드’를 운영하고 있다. 축사에 달린 센서를 통해 체중이 변하는 속도를 파악하고 분석하여 닭의 평균 체중, 건강 상태 등을 실시간으로 모니터링 할 수 있다. 또한 수집된 가축 데이터를 통해 닭의 울음소리 및 행동 양상을 분석하여 이상징후를 빠르게 감지할 수 있다. 파이프트리는 국내 치킨 프랜차이즈 ‘처갓집’을 비롯해 대만의 최초 치킨 프렌차이즈 기업과도 협업을 하는 등 사업 저변을 확장하고 있다.\n",
            "<엠트리센>\n‘엠트리센’은 인공지능 기반의 양돈농가 관리 자동화시스템 ‘딥아이즈’를 운영하고 있다. 생체, 번식, 행동 등의 대규모 가축 데이터를 수집·분석하여 분만돈의 새끼돼지 분만 시기, 건강, 이상징후 등을 실시간으로 감지할 수 있는 시스템이다. 또한 분만돈의 행동 양상을 분석하고 번식 중 분비되는 호르몬 이상을 파악해 새끼돼지의 사산을 예방하는 등 양돈농가의 수익성 증대에 기여하고 있다. 엠트리센은 최근 국내 과학기술 최고 상인 장영실상에 선정되는 등 첨단기술을 접목한 생명체 산업에서 최선두 기업으로 자리를 굳히고 있다. \n",
            "<트랙팜>\n‘트랙팜’ 또한 스마트 양돈농가 관리 시스템을 운영하고 있다. 인공지능을 기반으로 돼지의 행동 양상, 수면, 식사, 배변 등 건강 데이터를 모니터링하는 시스템이다. 축사 내 설치된 인공지능 센서 및 카메라를 통해 수집한 가축 데이터를 분석하여 대시보드 형태의 정보를 제공한다. 관리자는 이를 활용하여 돼지 개체의 건강 상태를 확인하고 질병을 예방해 항생제 투입을 최소화하는 등 품질 및 생산성을 높일 수 있다. 트랙팜은 이처럼 모듈화된 축사로 최적화된 제어 시스템을 제공하는 등 농축산업 자동화에 앞장서고 있다.\n",
            "앞서 살펴본 스타트업들은 첨단기술(디지털·AI·로봇 등)과 농업의 접목을 통해 침체된 농업경쟁력을 회복시키고 스마트농업, 푸드테크 산업 등 농식품 신산업의 수출 전략화를 위한 기반을 마련하는 데 있어 다양한 면면을 보여주었다. 나아가 농업의 미래 동력인 청년 농업인 육성부터 기후변화, 농축산업계 침체 등의 솔루션에 이르기까지 다방면에서 긍정적인 효과를 가져올 수 있다는 기대를 불러왔다. \n",
            "농업 혁명으로 불리는 애그테크가 일상에 스며들고 있는 가운데, 기존 농업인들과 새로운 청년 세대의 융화 그리고 다양한 관련 기관과 정부의 노력이 뒷받침되어 더욱 빛나게 될 K-애그테크의 밝은 미래를 기대해 본다.",
            "중소벤처기업부 & 창업진흥원",
            "디지털 핫이슈\n\n\n\nK-STARTUP\n\n\n\n미래농업 생태계 구축의 핵심, K-애그테크\n\n\n\n농업과 첨단기술의 만남\n\n\n\n중소벤처기업부 창업진흥원",
            "최근 저출생과 관련해 다양한 이슈가 논의되고 있는 가운데, 농어촌의 고령화와 소멸 현상 또한 심각한 문제로 떠오르고 있다. 한편, 전 세계적 기후변화로 인한 식량 생산량의 감소에 ‘농업(agriculture)’과 ‘기술(technology)’을 접목한 애그테크(Ag-tech)가 위기 극복의 대안으로 주목받고 있다. 애그테크는 스마트농업의 기반을 이루는 농업 관련 기술의 총칭으로 인공지능(AI)·사물인터넷(IoT)·빅데이터 등 첨단 기술을 농작물의 생산과 유통 전 과정에 적용한 것이다. \n",
            "정부에서도 농업과 농촌의 활성화 및 기후변화 대비 등을 위해 많은 노력을 기울이고 있다. 농작업의 전 과정을 기계화하고, 자율주행 농업로봇 개발을 확대하는 등 첨단 과학기술을 활용한 현장 문제 해결에 나서기로 했다. 또한 식량자급률 제고 등 농업 분야 공공 연구개발(R&D)을 강화하고, 스마트농업 확산과 바이오 융복합 혁신 기술 개발을 통해 미래 신성장 동력 마련에 노력하고 있다. 미래의 식량을 책임질 애그테크의 중요성이 대두되는 가운데 이와 관련해 대한민국 농축산업의 밝은 미래를 이끌어갈 K-애그테크 스타트업을 알아본다.\n",
            "<파미레세>\n‘파미레세’는 AI를 기반으로 디지털 육종을 개발하는 기업이다. 디지털 육종이란 기존 육종의 핵심 과정을 인공지능으로 대체하는 기술을 뜻한다. 현재 파미레세는 딸기·고추 재배 등에 디지털 육종을 적용해 생산성과 효율성을 높이고 있으며, 기존의 육종 방식보다 빠르고 정밀하게 새로운 품종을 개량하고 있다. 또한 스마트팜 뿐만 아니라 다양한 재배 환경에서도 구현 가능한 고기능성 품종을 연구하고 있다. 파미레세는 지속가능한 농업을 위해 디지털 전환을 이루는 등 미래 농업을 선도하고 있다.\n",
            "<지엘아이엔에스>\n‘지엘아이엔에스’는 농기계에 활용되는 제어 모듈을 개발하는 기업이다. 하나의 기기에서 트랙터나 콤바인과 같은 농기계의 주행 및 작업 등을 개별적으로 제어할 수 있는 통합 시스템을 구축하고 있다. 또한 높은 수준의 차량 표준통신규격을 기반으로 신속하게 데이터를 처리할 수 있고, 빛 탐지 및 범위 측정 감지기 등 첨단기술을 활용해 자율주행 농기계로의 확장도 수월하다. 지엘아이엔에스는 농업 완전 자동화라는 목표 아래 대형 농기계 시장이 활성화된 해외 시장에도 진출할 계획이다.\n",
            "<아그모>\n‘아그모’도 농기계 자율주행 모빌리티를 개발하고 있다. 트랙터, 이앙기 등과 같은 기존에 사용하던 농기계에 ‘아그모 솔루션’ 키트를 부착해 자율주행 농기계로 사용할 수 있다. 한 번의 운행으로 경로 및 데이터를 학습해 이후의 작업은 자율주행으로 처리할 수 있으며, 후진, 유턴 등도 가능해 우리나라처럼 다각형의 농지가 많은 아시아 국가에 적합하다. 또한 운행 중에 토양 상태 및 작물 데이터 등을 파악하고 이를 기반으로 분석해 농업 솔루션을 제공한다. 아그모는 운전자가 개입하는 현재의 자율주행 모델에서 더 나아가 완전 무인 자율주행 모델을 목표로 박차를 가하고 있다.\n",
            "<네토그린>\n‘네토그린’은 머신러닝 기반 농업 데이터 플랫폼을 운영하는 기업이다. 전문적인 농업 지식 습득이나 시간 투자 등의 부담 없이 일반인도 안정적으로 운영할 수 있는 스마트팜 솔루션을 제공하고 있으며, 스마트팜 초기 비용을 줄여 진입장벽을 낮추고 있다. 수직 농장을 활용해 공간의 활용성을 높였고, 실내 농장의 장점을 살려 사시사철 재배할 수 있는 시스템을 구축해 수확량 또한 높였다. 농장 시설뿐만 아니라 시스템 및 유통망에 이르기까지 스마트팜 종합 솔루션을 통해 농업 패러다임을 바꾸고 있다.\n",
            "<에이아이에스>\n온실과 달리 노지는 재배 환경을 제어할 수 없기 때문에 수확량 및 생육 상태에 대해 정확히 예측하기 어렵다. 대한민국 토지 중 90% 이상인 노지를 활용해 솔루션을 제공하는 기업이 있다. ‘에이아이에스’는 알고리즘 기반 농작물 재배관리 플랫폼을 통해 노지에서도 작물이 잘 자랄 수 있는 조건 및 정보 서비스를 제공하고 있다. 전 세계의 작물 생육 데이터를 분석하여 햇빛·광합성·토양·수분 등 작물 재배에 적합한 조건을 추천한다. 재해 리스크 관리는 물론 다음 작기와 관련해 보완할 점을 분석하는 등 체계적인 스마트 농업 시스템을 제공하고 있다.\n",
            "<만나씨이에이>\n‘만나씨이에이’는 아쿠아포닉스 기반의 스마트팜을 구축하고 있다. 아쿠아포닉스는 물고기를 양식하는 과정에서 배출되는 암모니아를 활용해 식물 배양액으로 이용하고, 식물이 정화한 물로 다시 물고기를 키우는 방식이다. 토양재배에서 발생하는 박테리아 감염 및 병해충 피해를 줄일 수 있고, 농약 및 합성 물질을 사용하지 않아 유기농·친환경 작물 생산에 적합하다. 만나씨이에이는 최근 AI 로봇 기업 ‘슈어모빌리티’와 협업을 하는 등 스마트팜의 재배 효율성을 높이기 위해 매진하고 있다.\n",
            "<드림팜>\n‘드림팜’은 자동화 청정 재배시설인 '스마트팜 큐브'를 운영하고 있다. ICT를 활용해 제어할 수 있는 큐브형 스마트팜 시설로 농업이 어려운 곳에서도 작물을 재배할 수 있도록 개발했다. 물이 흐르면서도 일정하게 낮은 온도를 유지하거나 습도를 조절할 수 있어 까다로운 생육환경의 작물도 기를 수 있다. 주로 고추냉이, 루콜라, 로메인 등 저온성 작물들을 주력으로 내세우고 있으며, 중동처럼 날씨가 더운 나라에서도 이를 활용해 작물을 재배할 수 있다. 실제로 드림팜은 사우디, 카타르, 베트남 등에 스마트팜 큐브를 수출하는 등 해외 시장에서도 첨단 농업 기술력을 선보이고 있다.\n",
            "<퓨처커넥트>\n‘퓨처커넥트’는 IoT 기반 스마트팜 공급 및 신선채소 판매 플랫폼을 운영하는 기업이다. 도심 속에서도 재배 가능한 모듈형 스마트팜 설계 기술과 더불어 인공지능 기반 자동 재배 기술, 농장 생산망 모니터링 및 제어 등이 핵심 솔루션이다. 이를 기반으로 도심 유휴공간 곳곳에서 작물을 재배하고 실시간 수요량에 따라 공급하는 등 누구나 신선한 채소를 섭취할 수 있도록 서비스를 운영하고 있다. 또한 구축된 농장 생산망을 통해 대규모 사옥, 주거단지, 공유오피스 등에 구독 형태의 모종 배송 서비스를 제공하는 등 다양한 비즈니스 모델을 갖추고 있다.\n",
            "<넥스트온>\n‘넥스트온’은 세계 최초로 IoT 기반 수직형 스마트팜을 통해 딸기를 연중 재배에 성공했다. 자체 LED 기술을 통해 최소한의 전력으로 농작물 광합성에 필요한 광량을 공급하며, 온습도·바람 제어 시스템과 더불어 자동 관개 시스템을 통해 유속 및 유량을 조절해 재배가 까다로운 작물도 재배할 수 있도록 한다. 또한 현대 미술 작가들과 협업을 통해 도심 속 스마트팜과 예술을 결합하여 관광객들의 이목을 끄는 등 단순 농장이 아닌 산업 관광으로서의 성장 가능성도 보여주고 있다. \n",
            "<아이오크롭스>\n‘아이오크롭스’는 인공지능을 기반으로 재배 및 데이터 수집·분석, 경영 관리까지 가능한 농작업 로봇을 개발하고 있다. 온실을 완전 자율 주행하는 로봇을 통해 자동으로 농장의 데이터를 수집할 수 있고, 이를 통해 다양한 온실 작물을 실시간으로 모니터링 하며 생장 상태를 확인할 수 있다. 로봇이 수집한 데이터를 통해 생육 지표를 분석하고, 이를 활용해 과실의 당도, 크기 및 수량 등을 예측할 수 있다. 아이오크롭스는 병해충 탐지 및 수확·운반 등에 이르기까지 완전 무인 자동화 시스템을 구축해 나갈 계획이다.\n",
            "<파이프트리>\n‘파이프트리’는 인공지능을 기반으로 양계농가의 질병 예찰 및 관리 시스템 ‘파머스 마인드’를 운영하고 있다. 축사에 달린 센서를 통해 체중이 변하는 속도를 파악하고 분석하여 닭의 평균 체중, 건강 상태 등을 실시간으로 모니터링 할 수 있다. 또한 수집된 가축 데이터를 통해 닭의 울음소리 및 행동 양상을 분석하여 이상징후를 빠르게 감지할 수 있다. 파이프트리는 국내 치킨 프랜차이즈 ‘처갓집’을 비롯해 대만의 최초 치킨 프렌차이즈 기업과도 협업을 하는 등 사업 저변을 확장하고 있다.\n",
            "<엠트리센>\n‘엠트리센’은 인공지능 기반의 양돈농가 관리 자동화시스템 ‘딥아이즈’를 운영하고 있다. 생체, 번식, 행동 등의 대규모 가축 데이터를 수집·분석하여 분만돈의 새끼돼지 분만 시기, 건강, 이상징후 등을 실시간으로 감지할 수 있는 시스템이다. 또한 분만돈의 행동 양상을 분석하고 번식 중 분비되는 호르몬 이상을 파악해 새끼돼지의 사산을 예방하는 등 양돈농가의 수익성 증대에 기여하고 있다. 엠트리센은 최근 국내 과학기술 최고 상인 장영실상에 선정되는 등 첨단기술을 접목한 생명체 산업에서 최선두 기업으로 자리를 굳히고 있다. \n",
            "<트랙팜>\n‘트랙팜’ 또한 스마트 양돈농가 관리 시스템을 운영하고 있다. 인공지능을 기반으로 돼지의 행동 양상, 수면, 식사, 배변 등 건강 데이터를 모니터링하는 시스템이다. 축사 내 설치된 인공지능 센서 및 카메라를 통해 수집한 가축 데이터를 분석하여 대시보드 형태의 정보를 제공한다. 관리자는 이를 활용하여 돼지 개체의 건강 상태를 확인하고 질병을 예방해 항생제 투입을 최소화하는 등 품질 및 생산성을 높일 수 있다. 트랙팜은 이처럼 모듈화된 축사로 최적화된 제어 시스템을 제공하는 등 농축산업 자동화에 앞장서고 있다.\n",
            "앞서 살펴본 스타트업들은 첨단기술(디지털·AI·로봇 등)과 농업의 접목을 통해 침체된 농업경쟁력을 회복시키고 스마트농업, 푸드테크 산업 등 농식품 신산업의 수출 전략화를 위한 기반을 마련하는 데 있어 다양한 면면을 보여주었다. 나아가 농업의 미래 동력인 청년 농업인 육성부터 기후변화, 농축산업계 침체 등의 솔루션에 이르기까지 다방면에서 긍정적인 효과를 가져올 수 있다는 기대를 불러왔다. \n",
            "농업 혁명으로 불리는 애그테크가 일상에 스며들고 있는 가운데, 기존 농업인들과 새로운 청년 세대의 융화 그리고 다양한 관련 기관과 정부의 노력이 뒷받침되어 더욱 빛나게 될 K-애그테크의 밝은 미래를 기대해 본다.",
            "중소벤처기업부 & 창업진흥원"
        ]
    }
]

def createJson_chat(conversation, file_path):
    data = {"messages": []}
    for question, answer in conversation:
        data["messages"].append({"role": "system", "content": "You are a chatbot called G-Bot of a friendly foreigner startup support platform"})
        data["messages"].append({"role": "user", "content": question})
        data["messages"].append({"role": "assistant", "content": answer})

    with open(file_path, "a", encoding="utf-8") as jsonl_file:
        jsonl_file.write(json.dumps(data, ensure_ascii=False) + "\n")
        
        
def auto_text_to_finetuning_data(text, save_path):

    keywords = []
    contents = []
    for i in range(len(raw_data)):
        for j in range(len(raw_data[i]["contents"])):
            
            text = raw_data[i]["contents"][j]

            match = re.search(r'<(.*?)>', text)

            if match:
                keyword = re.findall(r'<(.*?)>', text)[0]

                first_index = text.find(keyword)
                second_index = text.find(keyword, first_index + 1)

                content = text[second_index-1:]

                if keyword not in keywords:
                    keywords.append(keyword)
                    contents.append(content)


    if len(keywords) != len(contents):
        print("data extractoin failed")
        
    for i in range(len(keywords)):

        keyword, content = keywords[i], contents[i]

        last_char = keyword[-1]  
        jongsung = (ord(last_char) - 0xAC00) % 28  

        if jongsung == 0: 
            keyword_aug_list = [
                keyword,
                keyword + "가 뭐야?",
                keyword + "에 대해 설명해줘",
                keyword + "란?"
            ]
        else:  
            keyword_aug_list = [
                keyword,
                keyword + "이 뭐야?",
                keyword + "에 대해 설명해줘",
                keyword + "이란?"
            ]

        for keyword_aug in keyword_aug_list:
            createJson_chat([(keyword_aug, content)], save_path)
            
            

auto_text_to_finetuning_data(raw_data, save_path)

OPENAI_API_KEY = "put API KEY"
client = OpenAI(
    api_key= OPENAI_API_KEY
)

train_file = client.files.create(
    file=Path("./auto_data.jsonl"),
    purpose="fine-tune",
)

client.fine_tuning.jobs.create(
    training_file=train_file.id,
    model="gpt-3.5-turbo",
    hyperparameters={
    "n_epochs":13
  }
)

completion = client.chat.completions.create(
    model = "finetuned model",
    messages = [
        {"role": "system", "content": "You are a chatbot called G-Bot of a friendly foreigner startup support platform"},
        {"role": "user", "content": "오파테크?"}
    ]
)

print(completion.choices[0].message)