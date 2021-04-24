package com.example.ubimobile

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import com.example.ubimobile.classdata.ParkingFloor
import com.example.ubimobile.classdata.ParkingFloorData
import com.example.ubimobile.classdata.UserData
import com.example.ubimobile.classdata.User_Parcelable
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
            var u_id = ""
            var u_name = ""
            thread {
                //EditText에 입력한 id와 pass로 json데이터를 만들기
                var jsonobj = JSONObject()
                jsonobj.put("id", username.text)
                jsonobj.put("password", password.text)

                Log.d("msg", "Login접속${username.text}")
                val site = "http://192.168.0.2:8000/loginAndroid"
                val json: String = jsonobj.toString()
                //접속하기위한 객체를 생성
                val client = OkHttpClient()
                Log.d("msg", "Login접속준비")
                val request: Request = Request.Builder()
                        .url(site)
                        .post(RequestBody.create(MediaType.parse("application/json"), json))
                        .build()
                Log.d("msg", "Login접속완료")
                //요청하기
                val response: Response = client.newCall(request).execute()
                val result = response.body()!!.string() //response의 body를 추출
                val root = JSONObject(result)
                Log.d("msg", "추출전")
                u_id = root.getString("u_id")
                Log.d("msg", "추출변환${u_id},$u_name")

                //인텐트를 생성
                var objIntent = Intent(this, MainActivity::class.java)
                var obj = User_Parcelable()
                obj.u_id = u_id
                obj.u_name = u_name
                objIntent.putExtra("myobj", obj)
                Log.d("msg", "intent전송${obj.u_id},${obj.u_name}")
                startActivity(objIntent)
                Log.d("msg", "intent전송완료")
            }
        }
    }
}