package com.example.ubimobile

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.view.View
import android.widget.Button
import kotlinx.android.synthetic.main.function_main.*

class FunctionActivity : AppCompatActivity(),View.OnClickListener {


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.function_main)


        btn_1?.setOnClickListener(this)


    }




    override fun onClick(v: View?) {
        if(v is Button){
            var mybtn = v as Button
            if(v.text.equals("UNLOCK")){
                v.setText("LOCK")
                //unlock()
            }else{
                v.setText("UNLOCK")
                //lock()
            }
        }

    }
    fun lock(){

    }
    fun unlock(){

    }

}