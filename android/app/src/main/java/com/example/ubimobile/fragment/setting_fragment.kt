package com.example.ubimobile.fragment

import android.graphics.Color
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import com.example.ubimobile.R
import com.example.ubimobile.classdata.UsersCarData
import kotlinx.android.synthetic.main.adminpage.*
import okhttp3.*
import org.json.JSONArray
import org.json.JSONObject
import kotlin.concurrent.thread

class setting_fragment : Fragment {

    constructor(){

    }
    //뷰를 생성
    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {

        val view = inflater.inflate(R.layout.driving_main,container,false)
        return view
    }
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        var u_id = arguments?.getString("u_id")
        var u_name = arguments?.getString("u_name")
        thread{
            var jsonobj = JSONObject()
            jsonobj.put("id",u_id)
            val site = "http://192.168.0.2:8000/UsersCarAndroid"
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
                var dto = UsersCarData(
                    jsonobj.getInt("uc_id"),
                    jsonobj.getString("u_id"), jsonobj.getString("uc_model"),
                    jsonobj.getString("uc_number"), jsonobj.getString("uc_color"),
                    jsonobj.getInt("uc_ditance"), jsonobj.getString("uc_repair"),
                    jsonobj.getString("uc_age")
                )
                activity!!.runOnUiThread {
                    insertid.text = dto.u_id
                    insertname.text = u_name
                    insertmodel.text = dto.uc_model
                    insertnum.text = dto.uc_number
                    insertcolor.text = dto.uc_color
                    insertdis.text = dto.uc_ditance.toString()
                    insertrepair.text = dto.uc_repair
                    insertage.text = dto.uc_age
                }

            }
        }
    }
    }