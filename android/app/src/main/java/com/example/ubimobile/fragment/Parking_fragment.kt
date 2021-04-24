package com.example.ubimobile.fragment

import android.graphics.Color
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import androidx.fragment.app.Fragment
import com.example.ubimobile.classdata.ParkData
import com.example.ubimobile.R
import kotlinx.android.synthetic.main.parking_main.*
import okhttp3.*
import org.json.JSONArray
import org.json.JSONObject
import kotlin.concurrent.thread

class Parking_fragment : Fragment {
//    lateinit var handler: Handler
    constructor(){

    }
    //뷰를 생성
    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {

        val view = inflater.inflate(R.layout.parking_main,container,false)
        return view
    }
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        var u_id = arguments?.getString("u_id")


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
            // 압력신호에서 데이터를 받으면 park 없으면 line으로 변경
            thread{
                var jsonobj = JSONObject()
                jsonobj.put("id",u_id)
                val site = "http://192.168.0.202:8000/ParkingAndroid"
                val json:String =jsonobj.toString()
                //접속하기위한 객체를 생성
                val client = OkHttpClient()
                //Request 정보를 담은 Request객체 만들기
                val request: Request = Request.Builder()
                        .url(site)
                        .post(RequestBody.create(MediaType.parse("application/json"),json))
                        .build()
                //요청하기
                val response: Response = client.newCall(request).execute()
                val result = response.body()!!.string() //response의 body를 추출
                val root = JSONArray(result)
                for(i in 0 until root.length()){
                    //i번째 JSONObject를 추출해서 BoardData로 변환
                    var jsonobj = root.getJSONObject(i)
                    var dto = ParkData(
                        jsonobj.getInt("pf_id"),
                        jsonobj.getInt("p_id"), jsonobj.getInt("pf_floor"),
                        jsonobj.getInt("pf_space"), jsonobj.getInt("pf_data")
                    )
                    activity!!.runOnUiThread {
                        for(i in 1..3){
                            var resid = resources.getIdentifier("parkImg"+i,"id",
                                    activity?.applicationContext?.packageName)
                            if(dto.pf_floor == 1){
                                if(dto.pf_space == i) {
                                    if (dto.pf_data == 1) {
                                        view.findViewById<ImageView>(resid).setImageResource(R.drawable.park1)
                                    } else {
                                        view.findViewById<ImageView>(resid).setImageResource(R.drawable.line1)
                                    }
                                }
                        }
                        }
                        for(i in 4..6){
                            var resid = resources.getIdentifier("parkImg"+i,"id",
                                    activity?.applicationContext?.packageName)
                            if(dto.pf_floor == 1){
                                if(dto.pf_space == i) {
                                    if (dto.pf_data == 1) {
                                        view.findViewById<ImageView>(resid).setImageResource(R.drawable.park2)
                                    } else {
                                        view.findViewById<ImageView>(resid).setImageResource(R.drawable.line2)
                                    }
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
            thread{
                var jsonobj = JSONObject()
                jsonobj.put("id",u_id)
                val site = "http://192.168.0.202:8000/ParkingAndroid"
                val json:String =jsonobj.toString()
                //접속하기위한 객체를 생성
                val client = OkHttpClient()
                //Request 정보를 담은 Request객체 만들기
                val request: Request = Request.Builder()
                        .url(site)
                        .post(RequestBody.create(MediaType.parse("application/json"),json))
                        .build()
                //요청하기
                val response: Response = client.newCall(request).execute()
                val result = response.body()!!.string() //response의 body를 추출
                val root = JSONArray(result)
                for(i in 0 until root.length()){
                    //i번째 JSONObject를 추출해서 BoardData로 변환
                    var jsonobj = root.getJSONObject(i)
                    var dto = ParkData(
                        jsonobj.getInt("pf_id"),
                        jsonobj.getInt("p_id"), jsonobj.getInt("pf_floor"),
                        jsonobj.getInt("pf_space"), jsonobj.getInt("pf_data")
                    )
                    activity!!.runOnUiThread {
                        for(i in 7..9){
                            var resid = resources.getIdentifier("parkImg"+(i-6),"id",
                                    activity?.applicationContext?.packageName)
                            if(dto.pf_floor == 2){
                                if(dto.pf_space == i-6) {
                                    if (dto.pf_data == 1) {
                                        view.findViewById<ImageView>(resid).setImageResource(R.drawable.park1)
                                    } else {
                                        view.findViewById<ImageView>(resid).setImageResource(R.drawable.line1)
                                    }
                                }
                            }
                        }
                        for(i in 10..12){
                            var resid = resources.getIdentifier("parkImg"+(i-6),"id",
                                    activity?.applicationContext?.packageName)
                            if(dto.pf_floor == 2){
                                if(dto.pf_space == i-6) {
                                    if (dto.pf_data == 1) {
                                        view.findViewById<ImageView>(resid).setImageResource(R.drawable.park2)
                                    } else {
                                        view.findViewById<ImageView>(resid).setImageResource(R.drawable.line2)
                                    }
                                }
                            }
                        }
                    }

                }
            }
        }
    }
}