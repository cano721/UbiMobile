package com.example.ubimobile

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import androidx.fragment.app.Fragment


import com.example.ubimobile.sensor.MyMqtt




import kotlinx.android.synthetic.main.function_main.*

class function_fragment : Fragment {
    lateinit var mqttClient:MyMqtt //박수민추가
    constructor(){

    }
    //뷰를 생성
    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {

        val view = inflater.inflate(R.layout.function_main,container,false)
        return view

    }
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        btn_1?.setOnClickListener {
            if (btn_1.text == "UNLOCK"){
                btn_1.text = "LOCK"
            }
            else{
                btn_1.text = "UNLOCK"
            }
        }
    }




}