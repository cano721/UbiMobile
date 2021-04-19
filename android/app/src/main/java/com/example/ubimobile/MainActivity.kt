package com.example.ubimobile

import android.graphics.Color
import android.os.Bundle
import android.util.Log
import android.view.View
import androidx.core.content.ContextCompat
import androidx.fragment.app.Fragment
import androidx.fragment.app.FragmentActivity
import androidx.viewpager2.adapter.FragmentStateAdapter
import com.example.ubimobile.sensor.MyMqtt
import com.google.android.material.tabs.TabLayoutMediator
import kotlinx.android.synthetic.main.activity_main.*
import kotlinx.android.synthetic.main.function_main.*
import org.eclipse.paho.client.mqttv3.MqttMessage
import java.lang.Exception

<<<<<<< HEAD
class MainActivity : FragmentActivity(), View.OnClickListener {
    lateinit var mqttClient : MyMqtt //박수민추가
    val driving_view = Driving_fragment()
=======
class MainActivity : FragmentActivity() {
    val driving_view = DriveCamFragment()
>>>>>>> 195f182d12e2b5fae8ac83a3b28261275e0814d2
    val function_view = function_fragment()
    val setting_view = setting_fragment()
    val parking_view = Parking_fragment()
    val more_view = Driving_fragment()
    var fragmentList = ArrayList<Fragment>()
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
//        val driving_tab = findViewById<TabItem>(R.id.driving_tab)
//        val function_tab = findViewById<TabItem>(R.id.function_tab)
//        val car_setting_tab = findViewById<TabItem>(R.id.car_setting_tab)
//        val parking_tab = findViewById<TabItem>(R.id.parking_tab)
        fragmentList.add(driving_view)
        fragmentList.add(function_view)
        fragmentList.add(setting_view)
        fragmentList.add(parking_view)
        fragmentList.add(more_view)
//        fragmentList.add(driving_view)
//        fragmentList.add(driving_view)
//        fragmentList.add(driving_view)

        val adapter = object : FragmentStateAdapter(this) {
            override fun getItemCount(): Int {
                return fragmentList.size
            }

            override fun createFragment(position: Int): Fragment {
                return fragmentList[position]
            }

        }
        viewPager2.adapter = adapter

        TabLayoutMediator(tabs,viewPager2){tab, position ->
            when(position){
                0 -> {
                    tab.text = "주행화면"
                    tab.icon = ContextCompat.getDrawable(this, R.drawable.drivig_icon);
                }
                1 -> {
                    tab.text = "기능"
                    tab.icon = ContextCompat.getDrawable(this, R.drawable.function_icon);
                }
                2 -> {
                    tab.text = "차량관리"
                    tab.icon = ContextCompat.getDrawable(this, R.drawable.car_setting_icon);
                }
                3 -> {
                    tab.text = "주차"
                    tab.icon = ContextCompat.getDrawable(this, R.drawable.parking_icon);
                }
                4 -> {
                    tab.text = "더보기"
                    tab.icon = ContextCompat.getDrawable(this, R.drawable.more_icon);
                }
            }
        }.attach()

        mqttClient = MyMqtt(this,"tcp://172.30.1.3:1883")//박수민추가
        try {
            mqttClient.setCallback(::onReceived)
            mqttClient.connect(arrayOf<String>("iot/#"))
        }catch (e: Exception){
            e.printStackTrace()
        }
        klaxon.setOnClickListener(this)
        imageButton5.setOnClickListener(this)
    }
    fun onReceived(topic:String,message:MqttMessage){//박수민추가
        val msg = String(message.payload)
        Log.d("mymqtt",msg)
    }

    fun publish(data:String){//박수민추가
        mqttClient.publish("mydata/buzzer",data)

    }

    override fun onClick(v: View?) {//박수민추가
        var data:String = ""
        if(v?.id==R.id.klaxon){
            data="buzzer_on"
        }else{
            data="buzzer_off"
        }
        publish(data)
    }

}