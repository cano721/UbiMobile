package com.example.ubimobile

import android.graphics.Color
import android.os.Bundle

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup

import androidx.fragment.app.Fragment


import com.example.ubimobile.sensor.MyMqtt




import kotlinx.android.synthetic.main.function_main.*
import kotlinx.android.synthetic.main.parking_main.*
import org.eclipse.paho.client.mqttv3.MqttMessage
import java.util.*

class function_fragment : Fragment {
    lateinit var mqttClient:MyMqtt //박수민추가
    constructor(){

    }
    //뷰를 생성
    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {

        val view = inflater.inflate(R.layout.function_main,container,false)
        return view

    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        mqttClient = MyMqtt(activity!!.applicationContext,"tcp://172.30.1.56:1883")
        try {
            mqttClient.setCallback(::onReceived)
            mqttClient.connect(arrayOf<String>("iot/#"))
        }catch (e:Exception){
            e.printStackTrace()
        }
    }

    fun publish(data:String){
        //mqttClient 의 publish기능의의 메소드를 호출
        mqttClient.publish("mydata/function",data)
    }

    fun onReceived(topic:String,message:MqttMessage){
        val msg = String(message.payload)
    }


    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        btn_1?.setOnClickListener {
            var data:String = ""
            if (btn_1.text == "UNLOCK"){
                btn_1.text = "LOCK"
                btn_1.setTextColor(Color.parseColor("#EC6C3D"))
                data = "LOCK"
            }
            else{
                btn_1.text = "UNLOCK"
                btn_1.setTextColor(Color.parseColor("#FFFFFF"))
                data = "UNLOCK"
            }
            publish(data)
        }
        klaxon.setOnClickListener {
            var data: String = ""
            if (textView8.currentTextColor == Color.parseColor("#FFFFFF")) {
                data = "buzzer_on"
                textView8.setTextColor(Color.parseColor("#EC6C3D"))
            } else {
                data = "buzzer_off"
                textView8.setTextColor(Color.parseColor("#FFFFFF"))
            }
            publish(data)
        }
        switch1.setOnClickListener{
            var data:String = ""
            if(switch1.isChecked){
                data = "pulse_on"
            }else{
                data = "pulse_off"
            }
            publish(data)
        }
    }
}
