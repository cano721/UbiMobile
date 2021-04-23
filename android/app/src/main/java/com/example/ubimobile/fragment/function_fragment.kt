package com.example.ubimobile.fragment


import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.content.Context
import android.graphics.BitmapFactory
import android.graphics.Color
import android.os.Build
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.core.app.NotificationCompat
import androidx.core.content.ContextCompat
import androidx.fragment.app.Fragment
import com.example.ubimobile.R
import com.example.ubimobile.sensor.MyMqtt
import kotlinx.android.synthetic.main.function_main.*
import org.eclipse.paho.client.mqttv3.MqttMessage

class function_fragment : Fragment {
    lateinit var mqttClient: MyMqtt //박수민추가

    constructor() {

    }

    //뷰를 생성
    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {

        val view = inflater.inflate(R.layout.function_main, container, false)
        return view

    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        mqttClient = MyMqtt(activity!!.applicationContext, "tcp://192.168.0.202:1883")
        try {
            mqttClient.setCallback(::onReceived)
            mqttClient.connect(arrayOf<String>("iot/#"))
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    fun publish(data: String) {
        //mqttClient 의 publish기능의의 메소드를 호출
        mqttClient.publish("mydata/function", data)
    }

    fun onReceived(topic: String, message: MqttMessage) {
        val msg = String(message.payload)
        if(msg.equals("shocked")){
            val bitmap = BitmapFactory.decodeResource(resources,R.drawable.caracc)
            var builder = NotificationCompat.Builder(activity!!.applicationContext,"2222")
                    .setSmallIcon(R.drawable.ic_caracc)
                    .setContentTitle("차량충돌")
                    .setContentText("충돌알람")
                    .setPriority(NotificationCompat.PRIORITY_DEFAULT)
                    .setLargeIcon(bitmap)
                    .setDefaults(
                            Notification.DEFAULT_SOUND or Notification.DEFAULT_VIBRATE or
                                    Notification.DEFAULT_LIGHTS)
            val style = NotificationCompat.BigPictureStyle(builder)
            style.bigPicture(bitmap)
            builder.setStyle(style)
            createNotiChannel(builder,"2222")

        }
    }
    fun createNotiChannel(builder: NotificationCompat.Builder, id:String){
        //낮은 버전의 사용자에 대한 설정
        if(Build.VERSION.SDK_INT >= Build.VERSION_CODES.O){
            val channel = NotificationChannel(id, "mynetworkchannel", NotificationManager.IMPORTANCE_HIGH)
            val notificationManager = activity?.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
            notificationManager.createNotificationChannel(channel)
            notificationManager.notify(Integer.parseInt(id),builder.build())
        }else{
            val notificationManager = activity?.getSystemService(Context.NOTIFICATION_SERVICE)as NotificationManager
            notificationManager.notify(Integer.parseInt(id),builder.build())
        }
    }


    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        btn_1?.setOnClickListener {
            var data: String = ""
            if (btn_1.text == "UNLOCK") {
                btn_1.text = "LOCK"
                btn_1.setTextColor(Color.parseColor("#EC6C3D"))
                data = "LOCK"
            } else {
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
        switch1.setOnClickListener {//맥박센서퍼블리쉬
            var data: String = ""
            if (switch1.isChecked) {
                data = "pulse_on"
            } else {
                data = "pulse_off"
            }
            publish(data)
        }
        switch2.setOnClickListener {//충격센서
            var data: String = ""
            if (switch2.isChecked) {
                data = "shock_on"
            } else {
                data = "shock_off"
            }
            publish(data)
        }
        headlight.setOnClickListener {
            var data: String = ""
            if (text_headlight.currentTextColor == Color.parseColor("#FFFFFF")) {
                data = "LED_ON"
                text_headlight.setTextColor(Color.parseColor("#EC6C3D"))
            } else {
                data = "LED_OFF"
                text_headlight.setTextColor(Color.parseColor("#FFFFFF"))
            }
            publish(data)
        }
    }
}
