package com.example.ubimobile.fragment

import android.app.Notification
import android.content.Context
import android.graphics.BitmapFactory
import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.MotionEvent
import android.view.View
import android.view.ViewGroup
import android.widget.SeekBar
import androidx.core.app.NotificationCompat
import androidx.core.content.ContextCompat
import androidx.fragment.app.Fragment
import com.example.ubimobile.R
import com.example.ubimobile.sensor.MyMqtt
import org.eclipse.paho.client.mqttv3.MqttMessage
import kotlinx.android.synthetic.main.fragment_drive_cam.*
import org.json.JSONObject


class DriveCamFragment : Fragment() {
    lateinit var mqttClient: MyMqtt
    private val flaskUrl: String = "http://192.168.200.127:8088/off"
    private var stat_manual: Boolean = false
    private val speed: Int = 50
    private val ratio: Double = 0.5

    override fun onAttach(context: Context) {
        super.onAttach(context)
        Log.d("lifecycle","Fragment:::::::DriveCam_onAttach()")
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        Log.d("lifecycle","Fragment:::::::DriveCam_onCreate()")

        mqttClient = MyMqtt(activity!!.applicationContext, "tcp://192.168.0.202:1883")

        try {
            mqttClient.connect(arrayOf<String>("iot/#"))
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    fun publish(data: String) {
        mqttClient.publish("ubimobile/motor", data)
    }

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        Log.d("lifecycle","Fragment:::::::DriveCam_onCreateView()")
        val view = inflater.inflate(R.layout.fragment_drive_cam,container,false)
        return view
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        Log.d("lifecycle","Fragment:::::::DriveCam_onViewCreated()")
        var data: String = ""
        set_manual.setOnClickListener {
            data = """
                {
                    "command": "manual"
                }
            """.trimIndent()
            publish(data)
            stat_manual = true
            set_manual.isEnabled = false
            set_manual.setTextColor(ContextCompat.getColor(context!!, R.color.yellow_700))
            manual_layout.visibility = View.VISIBLE
            set_auto.isEnabled = true
            set_manual.setTextColor(ContextCompat.getColor(context!!, R.color.white))
            auto_layout.visibility = View.INVISIBLE
            web_view_cam.loadUrl("$flaskUrl/off")
        }

        set_auto.setOnClickListener{
            data = """
                {
                    "command": "auto"
                }
            """.trimIndent()
            publish(data)
            stat_manual = false
            set_manual.isEnabled = true
            set_manual.setTextColor(ContextCompat.getColor(context!!, R.color.white))
            manual_layout.visibility = View.INVISIBLE
            set_auto.isEnabled = false
            set_manual.setTextColor(ContextCompat.getColor(context!!, R.color.yellow_700))
            auto_layout.visibility = View.VISIBLE
            web_view_cam.loadUrl("$flaskUrl/on")
        }

        set_camera.setOnClickListener {
            if (stat_manual) {
                web_view_cam.loadUrl("$flaskUrl/off")
            }
            else {
                web_view_cam.loadUrl("$flaskUrl/on")
            }
        }

        manual_Front.setOnTouchListener(object : View.OnTouchListener {
            override fun onTouch(v: View?, event: MotionEvent?): Boolean {
                when (event?.action) {
                    MotionEvent.ACTION_DOWN -> {
                        data = """
                            {
                                "speed": $speed
                            }
                        """.trimIndent()
                        publish(data)
                    }
                    MotionEvent.ACTION_UP -> {
                        data = """
                            {
                                "speed": 0
                            }
                        """.trimIndent()
                        publish(data)
                    }
                }
                return v?.onTouchEvent(event) ?: true
            }
        })
        manual_back.setOnTouchListener(object : View.OnTouchListener {
            override fun onTouch(v: View?, event: MotionEvent?): Boolean {
                when (event?.action) {
                    MotionEvent.ACTION_DOWN -> {
                        data = """
                            {
                                "speed": -$speed
                            }
                        """.trimIndent()
                        publish(data)
                    }
                    MotionEvent.ACTION_UP -> {
                        data = """
                            {
                                "speed": 0
                            }
                        """.trimIndent()
                        publish(data)
                    }
                }
                return v?.onTouchEvent(event) ?: true
            }
        })
        manual_left.setOnTouchListener(object : View.OnTouchListener {
            override fun onTouch(v: View?, event: MotionEvent?): Boolean {
                when (event?.action) {
                    MotionEvent.ACTION_DOWN -> {
                        data = """
                            {
                                "speed": $speed
                                "leftRatio": 0
                            }
                        """.trimIndent()
                        publish(data)
                    }
                    MotionEvent.ACTION_UP -> {
                        data = """
                            {
                                "speed": 0
                            }
                        """.trimIndent()
                        publish(data)
                    }
                }
                return v?.onTouchEvent(event) ?: true
            }
        })
        manual_right.setOnTouchListener(object : View.OnTouchListener {
            override fun onTouch(v: View?, event: MotionEvent?): Boolean {
                when (event?.action) {
                    MotionEvent.ACTION_DOWN -> {
                        data = """
                            {
                                "speed": $speed
                                "rightRatio": 0
                            }
                        """.trimIndent()
                        publish(data)
                    }
                    MotionEvent.ACTION_UP -> {
                        data = """
                            {
                                "speed": 0
                            }
                        """.trimIndent()
                        publish(data)
                    }
                }
                return v?.onTouchEvent(event) ?: true
            }
        })
        manual_leftCurve.setOnTouchListener(object : View.OnTouchListener {
            override fun onTouch(v: View?, event: MotionEvent?): Boolean {
                when (event?.action) {
                    MotionEvent.ACTION_DOWN -> {
                        data = """
                            {
                                "speed": $speed
                                "leftRatio": $ratio
                            }
                        """.trimIndent()
                        publish(data)
                    }
                    MotionEvent.ACTION_UP -> {
                        data = """
                            {
                                "speed": 0
                            }
                        """.trimIndent()
                        publish(data)
                    }
                }
                return v?.onTouchEvent(event) ?: true
            }
        })
        manual_rightCurve.setOnTouchListener(object : View.OnTouchListener {
            override fun onTouch(v: View?, event: MotionEvent?): Boolean {
                when (event?.action) {
                    MotionEvent.ACTION_DOWN -> {
                        data = """
                            {
                                "speed": $speed
                                "rightRatio": $ratio
                            }
                        """.trimIndent()
                        publish(data)
                    }
                    MotionEvent.ACTION_UP -> {
                        data = """
                            {
                                "speed": 0
                            }
                        """.trimIndent()
                        publish(data)
                    }
                }
                return v?.onTouchEvent(event) ?: true
            }
        })
        manual_leftBack.setOnTouchListener(object : View.OnTouchListener {
            override fun onTouch(v: View?, event: MotionEvent?): Boolean {
                when (event?.action) {
                    MotionEvent.ACTION_DOWN -> {
                        data = """
                            {
                                "speed": -$speed
                                "leftRatio": $ratio
                            }
                        """.trimIndent()
                        publish(data)
                    }
                    MotionEvent.ACTION_UP -> {
                        data = """
                            {
                                "speed": 0
                            }
                        """.trimIndent()
                        publish(data)
                    }
                }
                return v?.onTouchEvent(event) ?: true
            }
        })
        manual_rightBack.setOnTouchListener(object : View.OnTouchListener {
            override fun onTouch(v: View?, event: MotionEvent?): Boolean {
                when (event?.action) {
                    MotionEvent.ACTION_DOWN -> {
                        data = """
                            {
                                "speed": -$speed
                                "rightRatio": $ratio
                            }
                        """.trimIndent()
                        publish(data)
                    }
                    MotionEvent.ACTION_UP -> {
                        data = """
                            {
                                "speed": 0
                            }
                        """.trimIndent()
                        publish(data)
                    }
                }
                return v?.onTouchEvent(event) ?: true
            }
        })
        auto_seekBar_distance.setOnSeekBarChangeListener(object : SeekBar.OnSeekBarChangeListener{
            override fun onProgressChanged(seekBar: SeekBar?, progress: Int, fromUser: Boolean) {
                auto_text_distance.text = auto_seekBar_distance.progress.toString() + " cm"
            }

            override fun onStartTrackingTouch(seekBar: SeekBar?) {
                TODO("Not yet implemented")
            }

            override fun onStopTrackingTouch(seekBar: SeekBar?) {
                TODO("Not yet implemented")
            }
        })
        auto_seekBar_velocity.setOnSeekBarChangeListener(object : SeekBar.OnSeekBarChangeListener{
            override fun onProgressChanged(seekBar: SeekBar?, progress: Int, fromUser: Boolean) {
                auto_text_velocity.text = auto_seekBar_velocity.progress.toString()
            }

            override fun onStartTrackingTouch(seekBar: SeekBar?) {
                TODO("Not yet implemented")
            }

            override fun onStopTrackingTouch(seekBar: SeekBar?) {
                TODO("Not yet implemented")
            }
        })
        auto_lane_left.setOnClickListener {

        }
        auto_lane_right.setOnClickListener {
            
        }
    }

    override fun onActivityCreated(savedInstanceState: Bundle?) {
        super.onActivityCreated(savedInstanceState)
        Log.d("lifecycle","Fragment:::::::DriveCam_onActivityCreated()")
    }

    override fun onStart() {
        super.onStart()
        Log.d("lifecycle","Fragment:::::::DriveCam_onStart()")
    }

    override fun onResume() {
        super.onResume()
        Log.d("lifecycle","Fragment:::::::DriveCam_onResume()")
        web_view_cam.loadUrl("$flaskUrl/off")
    }

    override fun onPause() {
        super.onPause()
        Log.d("lifecycle","Fragment:::::::DriveCam_onPause()")
    }

    override fun onStop() {
        super.onStop()
        Log.d("lifecycle","Fragment:::::::DriveCam_onStop()")
    }

    override fun onDestroyView() {
        super.onDestroyView()
        Log.d("lifecycle","Fragment:::::::DriveCam_onDestroyView()")
    }

    override fun onDestroy() {
        super.onDestroy()
        Log.d("lifecycle","Fragment:::::::DriveCam_onDestroy()")
    }

    override fun onDetach() {
        super.onDetach()
        Log.d("lifecycle","Fragment:::::::DriveCam_onDetach()")
    }
}