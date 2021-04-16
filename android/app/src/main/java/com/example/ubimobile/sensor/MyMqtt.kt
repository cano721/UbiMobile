package com.example.ubimobile.sensor

import android.content.Context
import android.util.Log
import org.eclipse.paho.android.service.MqttAndroidClient
import org.eclipse.paho.client.mqttv3.*

class MyMqtt(val context:Context,val uri:String) {
    var mqttClient:MqttAndroidClient = MqttAndroidClient(context,uri,MqttClient.generateClientId())
    fun setCallback(callback:(topic:String, message:MqttMessage)->Unit){
        //등록한 토픽에 맞는 메시지가 도착하면 사용자정의 메소드를 실행할수있도록 callback 구현 --3
        mqttClient.setCallback(object : MqttCallback{
            override fun messageArrived(topic: String?, message: MqttMessage?) {
                callback(topic!!,message!!)
            }

            override fun connectionLost(cause: Throwable?) {
                Log.d("mymqtt","connectionLost")
            }

            override fun deliveryComplete(token: IMqttDeliveryToken?) {
                 Log.d("mymqtt","deliveryComplete")
            }

        })
    }
    fun connect(topics: Array<String>?=null){
        val mqttconnect_options = MqttConnectOptions()
        //connect호출 - broker에 연결
        mqttClient.connect(mqttconnect_options,null,object : IMqttActionListener{
            override fun onSuccess(asyncActionToken: IMqttToken?) {
                Log.d("mymqtt","connect 성공")
              //서버로 전송 성공하면
                topics?.map{subscribeTopic(it)}
            }

            override fun onFailure(asyncActionToken: IMqttToken?, exception: Throwable?) {
                Log.d("mymqtt","connect 실패")
            }

        })
    }
    //topic subscriber 등록할 메소드'
    private fun subscribeTopic(topic:String,qos:Int=0){
        mqttClient.subscribe(topic,qos,null,object:IMqttActionListener{
            override fun onSuccess(asyncActionToken: IMqttToken?) {
                Log.d("mqtt","subscribe성공")
            }

            override fun onFailure(asyncActionToken: IMqttToken?, exception: Throwable?) {
                Log.d("mqtt","subscribe실패")
            }

        })
    }
    //broker에 publish할때 사용할 메소드
    fun publish(topic:String, payload:String, qos:Int=0){
        if(mqttClient.isConnected() === false){
            mqttClient.connect()

        }
        val message = MqttMessage()
        message.payload = payload.toByteArray() //String을 byte배열로 변환- 네트워크로 전송
        message.qos = qos
        mqttClient.publish(topic,message,null,object:IMqttActionListener{
            override fun onSuccess(asyncActionToken: IMqttToken?) {
                Log.d("mymqtt","publish 성공")
            }

            override fun onFailure(asyncActionToken: IMqttToken?, exception: Throwable?) {
                Log.d("mymqtt","publish 실패")
            }

        })
    }
}

