package com.example.ubimobile

import android.graphics.Color
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.os.Message
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
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
    lateinit var handler: Handler
    constructor(){

    }
    //뷰를 생성
    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {

        val view = inflater.inflate(R.layout.parking_main,container,false)
        return view
    }
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
//        handler = object : Handler(Looper.myLooper()!!){
//            override fun handleMessage(msg: Message) {
//                when(msg.what){
//                    0 -> view.findViewById<ImageView>(msg.arg1).setImageResource(R.drawable.line1)
//
//                    1 -> view.findViewById<ImageView>(msg.arg1).setImageResource(R.drawable.park1)
//
//                }
//            }
//        }
        firstFloor.setOnClickListener {
            Log.d("http","버튼클릭....")
            // 압력신호에서 데이터를 받으면 park 없으면 line으로 변경
            thread{
                Log.d("http","쓰레드진입....")
                val site = "http://192.168.0.202:8000/parkpage?{$id}"
                val url = URL(site)
                val con = url.openConnection() as HttpURLConnection

                val isr = InputStreamReader(con.inputStream,"UTF-8")
                val br = BufferedReader(isr)

                var str:String?
                var buf = StringBuffer()
                Log.d("http","웹서버 연결....")
                do {
                    str = br.readLine() //버퍼에 있는 모든 내용을 읽어오기 - 한 라인씩 읽기
                    Log.d("http","버퍼내용읽기....")
                    if (str != null) {
                        buf.append(str)
                    }
                }while (str!=null) //네트워크로 전송되는 데이터를 읽어서 StringBuffer에 저장하기
                val data = buf.toString()
                Log.d("http","스트링변환....")
                Log.d("http", "{$data}....")
                val root = JSONArray(data)
                Log.d("http","데이터저장....")
                for(i in 0 until root.length()){
                    //i번째 JSONObject를 추출해서 BoardData로 변환
                    var jsonobj = root.getJSONObject(i)
                    var dto = ParkData(jsonobj.getInt("pf_id"),
                            jsonobj.getInt("p_id"),jsonobj.getInt("pf_floor"),
                            jsonobj.getInt("pf_space"),jsonobj.getInt("pf_data"))
                    Log.d("http","데이터객체로변환....")
                    activity!!.runOnUiThread {
                        for(i in 1..6){
                            var resid = resources.getIdentifier("parkImg"+i+1,"id",
                                    activity?.applicationContext?.packageName)
                            if(dto.pf_id == i){
                                if(dto.pf_data == 1){
                                    view.findViewById<ImageView>(resid).setImageResource(R.drawable.park1)
                                }else{
                                    view.findViewById<ImageView>(resid).setImageResource(R.drawable.line1)
                                }
                        }
                        }
                    }

                }
            }
            firstFloor.setTextColor(Color.parseColor("#EC6C3D"))
            secondFloor.setTextColor(Color.parseColor("#FFFFFF"))
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