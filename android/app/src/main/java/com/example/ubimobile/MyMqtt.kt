package com.example.ubimobile

import android.content.Context
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import org.eclipse.paho.android.service.MqttAndroidClient
import org.eclipse.paho.client.mqttv3.*

class MyMqtt(val context: Context, val uri:String){
    var mqttClient:MqttAndroidClient = MqttAndroidClient(context,uri,MqttClient.generateClientId())

    fun setCallback(callback :(topic:String,message:MqttMessage)->Unit){
        mqttClient.setCallback(object:MqttCallback{
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
    fun connect(topics:Array<String>?=null){
        val mqttconnect_options = MqttConnectOptions()
        mqttClient.connect(mqttconnect_options,null,object :IMqttActionListener{
            override fun onSuccess(asyncActionToken: IMqttToken?) {
                Log.d("mymqtt","접속성공....")
                topics?.map { subscribeTopics(it) }
            }

            override fun onFailure(asyncActionToken: IMqttToken?, exception: Throwable?) {
                Log.d("mymqtt","접속실패")
            }
        })
    }
    private fun subscribeTopics(topic: String, qos:Int = 0){
        mqttClient.subscribe(topic, qos, null, object : IMqttActionListener{
            override fun onSuccess(asyncActionToken: IMqttToken?) {
                Log.d("mymqtt","subscribe성공")
            }

            override fun onFailure(asyncActionToken: IMqttToken?, exception: Throwable?) {
                Log.d("mymqtt","subscribe실패")
            }
        })
    }
    fun publish(topic: String, payload:String,qos: Int=0){
        if(mqttClient.isConnected() === false){
            mqttClient.connect()
        }
        val message = MqttMessage()
        message.payload = payload.toByteArray()
        message.qos = qos
        mqttClient.publish(topic,message,null,object :IMqttActionListener{
            override fun onSuccess(asyncActionToken: IMqttToken?) {
                Log.d("mymqtt","publish성공")
            }

            override fun onFailure(asyncActionToken: IMqttToken?, exception: Throwable?) {
                Log.d("mymqtt","publish실패")
            }
        })
    }
}















