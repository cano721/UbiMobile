package com.example.ubimobile

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.webkit.WebSettings
import kotlinx.android.synthetic.main.activity_drive_cam.*

class DriveCamActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_drive_cam)
        web_view_cam.loadUrl("http://192.168.200.127:8088")

    }
}