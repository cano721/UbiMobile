package com.example.ubimobile

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import com.example.ubimobile.classdata.ParkingFloor
import com.example.ubimobile.classdata.ParkingFloorData
import kotlinx.android.synthetic.main.activity_login.*
import okhttp3.*
import org.json.JSONArray
import org.json.JSONObject
import kotlin.concurrent.thread

class LoginActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_login)
        login.setOnClickListener {
            var pf_id = ""
            var pf_data = ""
//            var datalist = mutableListOf<>()
            thread{
                //EditText에 입력한 id와 pass로 json데이터를 만들기
                var jsonobj = JSONObject()
                jsonobj.put("id",username.text)
                jsonobj.put("password",password.text)
                val site = "http://192.168.0.202:8000/loginAndroid"
                val json:String =jsonobj.toString()
                //접속하기위한 객체를 생성
                val client = OkHttpClient()
                //Request 정보를 담은 Request객체 만들기

                /*var builder = Request.Builder()
                builder = builder.url("")
                builder = builder.post(null)
                val req = builder.build()
                 */

                val request:Request = Request.Builder()
                        .url(site)
                        .post(RequestBody.create(MediaType.parse("application/json"),json))
                        .build()
                //요청하기
                val response:Response = client.newCall(request).execute()
                val result = response.body()!!.string() //response의 body를 추출
                Log.d("msg","제이슨변환")
                val root = JSONArray(result)
                Log.d("msg","추출전$result")
                for(i in 0 until root.length()) {
                    //i번째 JSONObject를 추출해서 BoardData로 변환
                    var jsonobj = root.getJSONObject(i)
                    var data = mutableMapOf(jsonobj.getInt("pf_id").toString() to jsonobj.getInt("pf_data").toString())
//                    datalist.add(data)
                }
                Log.d("msg","추출변환$pf_id,$pf_data")
            }
            //인텐트를 생성
            var objIntent = Intent(this,MainActivity::class.java)
            var obj = ParkingFloor()
            obj.pf_id = pf_id
            obj.pf_data = pf_data
            objIntent.putExtra("myobj",obj)
            Log.d("msg","intent전송")
            startActivity(objIntent)
            Log.d("msg","intent전송완료")
        }
    }
}