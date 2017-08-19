# fileReader Write Up

BoB 6기 취약점 분석 트랙 정주영

사용 언어: python2.7 (flask)

site: [h4ck.kr](http://h4ck.kr)

## 코드 분석

총 4 종류의 route가 정의되어 있다.

### 1. "/"
메인 페이지이다.
```sh
@app.route('/')
def main():
    session.clear()
    lists = os.listdir('./files')
    return render_template('main.html', files=lists)
```

session정보를 모두 초기화 해 주고, ./files경로에 있는 파일 목록을 main.html에 넘겨준다.

### 2. "/readFile"
```sh
@app.route('/readFile', methods = ['GET'])
def openFile():
    fileName = request.args.get('fileName')

    #filter
    if fileName not in os.listdir('./files'):
        session.clear()
        return "file open fail"

    if session.get('fileFlag') == True:
        session.pop('fileData', None)
    session['fileFlag'] = True
    with open("files/" + fileName ,"r") as f:
        datas = f.readlines()
        data = "\n".join(i for i in datas)
    session['fileData'] = data

    return redirect('/checkFlag')
```

GET메소드로 파일 이름을 받는다. 
해당 파일을 열어 내용을 읽은 뒤, session['fileData']에 내용을 저장한다.

### 3. "/checkFlag"
```sh
@app.route('/checkFlag')
def checkIsFlag():
    data = session['fileData']
    session['flagChecked'] = True
    if check_is_flag(data) == 1:
        session['flagChecked'] = False
        session['fileFlag'] = False
        session.pop('fileData', None)
        return "You Cannot Open flag ^~^"
    return redirect('/result')
```

파일 내용을 check_is_flag 함수에 넘겨 flag의 내용과 같은지 확인한다.
파일 내용이 flag내용과 일치하지 않으면 /result로 redirect해준다.

#### check_is_flag
```sh
def check_is_flag(data):
    data = hashlib.sha256(data).hexdigest()

    if data == "c3065ded789a1f36072cd8d03b2c4626e3835419971078108e1f138396432d82":
        return 1
    return 0
```
sha256 돌려서 flag를 돌린 결과인 c3065ded789a1f36072cd8d03b2c4626e3835419971078108e1f138396432d82와 같은지 확인한다ㅏ.

### 4. "/result"
```sh
@app.route('/result')
def res():
    if session.get('fileFlag') != True:
        return "File Already Closed"
    if session.get('flagChecked') != True:
        return "Check your data first"
    data = session['fileData']
    session['fileFlag'] = False
    session['flagChecked'] = False
    session.pop('fileData', None)
    return data
```
session['fildData']의 내용을 출력해준다.

## 풀이

정리하자면, 파일을 열면 아래의 단계로 프로그램이 동작한다.

파일명클릭 -> 파일열어서 session['fileData'] 에 내용 저장 -> /checkFlag로 redirect -> sha256으로 flag를 연 내용과 같은지 체크 -> 같지 않으면 /result로 redirect -> 출력

따라서 /result로 redirect되기 직전에 다른 탭에서 flag를 열어 session['fileData']의 내용을 바꿔주면, flag의 내용을 알 수 있다.

flag: flag{p@55w0rcl_ls_53CR3T}
