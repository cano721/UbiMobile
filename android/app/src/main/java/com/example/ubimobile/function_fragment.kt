package com.example.ubimobile

import android.os.Bundle

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup

import androidx.fragment.app.Fragment


import com.example.ubimobile.sensor.MyMqtt




import kotlinx.android.synthetic.main.function_main.*
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
        mqttClient = MyMqtt(activity!!.applicationContext,"tcp://192.168.0.28:1883")
        try {
            mqttClient.setCallback(::onReceived)
            mqttClient.connect(arrayOf<String>("iot/#"))
        }catch (e:Exception){
            e.printStackTrace()
        }
      //  btn_1.setOnClickListener(this)
    }

  /*  override fun onClick(v: View?) {
        var data:String=""
        if(v?.id==R.id.btn_1){
            data = "UNLOCK"
        }else{
            data = "LOCK"
        }
        publish(data)
    }
*/
    fun publish(data:String){
        //mqttClient 의 publish기능의의 메소드를 호출
        mqttClient.publish("mydata/lock",data)
    }

    fun onReceived(topic:String,message:MqttMessage){
        val msg = String(message.payload)
    }


    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        var data:String = " "
        btn_1?.setOnClickListener {
            if (btn_1.text == "UNLOCK"){
                btn_1.text = "LOCK"
            }
            else{
                btn_1.text = "UNLOCK"
            }
            publish(data)
        }
    }
}
