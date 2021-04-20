package com.example.ubimobile

import android.content.Context
import android.graphics.Color
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.core.content.ContextCompat
import androidx.fragment.app.Fragment
import kotlinx.android.synthetic.main.parking_main.*
import kotlinx.android.synthetic.main.parking_main.view.*
import org.json.JSONArray
import java.io.BufferedReader
import java.io.InputStreamReader
import java.net.HttpURLConnection
import java.net.URL
import kotlin.concurrent.thread

class Parking_fragment : Fragment {

    constructor(){

    }
    //뷰를 생성
    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {

        val view = inflater.inflate(R.layout.parking_main,container,false)
        return view
    }
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        firstFloor.setOnClickListener {
            // 압력신호에서 데이터를 받으면 park 없으면 line으로 변경
            firstFloor.setTextColor(Color.parseColor("#EC6C3D"))
            secondFloor.setTextColor(Color.parseColor("#FFFFFF"))
//            thread{
//                //네트워크를 통해 데이터를 요청하는 경우는 무조건 쓰레드 처리한다.
//                //접속할 주소
//                val site = "http://192.168.0.202:8000/parkpage"
//                //주소를 사용할 수 있도록 객체로 정의
//                val url = URL(site)
//
//                //접속하기 - as ... 캐스팅 openConnection이 리턴하는 객체를 하위 객체(HttpURLConnection)로 변환
//                //URLConnection이 URLConnection을 리턴하지만 구체적인 기능을 사용하기 위해서 자식객체인
//                //HttpURLConnection으로 변경
//                val con = url.openConnection() as HttpURLConnection
//
//                //네트워크를 통해 전송되어오는 데이터를 읽어서 처리하기위한 안드로이드의 입력스트링클래스를
//                //선언하고 처리
//                //byte로 전송 -> 한글이 있으므로 문자단위 처리로 변경
//                //byte단위 처리 클래스로 문자단위 처리클래스를 생성
//                //InputStreamReader은 기본처리만 가능
//                val isr = InputStreamReader(con.inputStream,"UTF-8")
//                val br = BufferedReader(isr)
//
//                var str:String? = null //String으로 문자열을 표현하면 객체가 너무 만들어진다.
//                var buf = StringBuffer() //String보다 리소스를 적게 사용하므로 네트워크에서 처리되는 문자열은
//                //StringBuffer로 작업
//                do {
//                    str = br.readLine() //버퍼에 있는 모든 내용을 읽어오기 - 한 라인씩 읽기
//                    if (str != null) {
//                        buf.append(str)
//                    }
//                }while (str!=null) //네트워크로 전송되는 데이터를 읽어서 StringBuffer에 저장하기
//                val data = buf.toString()
//                //JSON객체를 파싱하는 작업을 처리
//                //JSONArray객체로 받아서 JSONArray에 저장된 JSONObject의 갯수만큼 처리
//                //[] ->json데이터에서 array
//                //{} -> json데이터에서 object
//
////                runOnUiThread {
////                    textView2.text = data
////                }
//                val root = JSONArray(data)
//                for(i in 0 until root.length()){
//                    //i번째 JSONObject를 추출해서 BoardData로 변환
//                    var jsonobj = root.getJSONObject(i)
//                    var dto = BoardData(jsonobj.getInt("boardNo"),
//                            jsonobj.getString("title"),jsonobj.getString("content"),
//                            jsonobj.getString("writer"),jsonobj.getString("write_date"))
//
//                    runOnUiThread {
//                        parkImg1.setImageResource(R.drawable.park1)
//                        parkImg2.setImageResource(R.drawable.park1)
//                        parkImg3.setImageResource(R.drawable.park1)
//                        parkImg4.setImageResource(R.drawable.park2)
//                        parkImg5.setImageResource(R.drawable.park2)
//                        parkImg6.setImageResource(R.drawable.park2)
//                    }
//
//                }
//            }
        }
        secondFloor.setOnClickListener {
            // 압력신호에서 데이터 받으면 park 없으면 line로 변경
            firstFloor.setTextColor(Color.parseColor("#FFFFFF"))
            secondFloor.setTextColor(Color.parseColor("#EC6C3D"))
            parkImg1.setImageResource(R.drawable.park1)
            parkImg2.setImageResource(R.drawable.park1)
            parkImg3.setImageResource(R.drawable.park1)
            parkImg4.setImageResource(R.drawable.park2)
            parkImg5.setImageResource(R.drawable.park2)
            parkImg6.setImageResource(R.drawable.park2)
        }
    }
}