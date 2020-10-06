package com.example.myapplication;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import android.Manifest;
import android.app.ActivityManager;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.Bundle;
<<<<<<< HEAD
import android.view.View;
import android.view.Window;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.Spinner;
=======
import android.os.Looper;
import android.view.View;
import android.view.Window;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Switch;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.gms.location.LocationCallback;
import com.google.android.gms.location.LocationRequest;
import com.google.android.gms.location.LocationResult;
import com.google.android.gms.location.LocationServices;

import java.sql.Time;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.time.Clock;
import java.util.Calendar;
import java.util.Date;
import java.util.Locale;
import java.util.Objects;
>>>>>>> 8f58b95ca63129ae98a1c65481e578685ce2585c

import androidx.appcompat.app.AppCompatActivity;

import com.intel.realsense.librealsense.DeviceListener;
import com.intel.realsense.librealsense.RsContext;

public class CameraActivity extends AppCompatActivity {
    private RsContext mRsContext;

    // Used to load the 'native-lib' library on application startup.
    static {
        System.loadLibrary("native-lib");
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        this.requestWindowFeature(Window.FEATURE_NO_TITLE);
        setContentView(R.layout.select_camera);

<<<<<<< HEAD
        // setting up all the spiners
        setupSpinners();

        final Button configure_camera = (Button) findViewById(R.id.configure_camera);
        RsContext.init(getApplicationContext());
        //Register to notifications regarding RealSense devices attach/detach events via the DeviceListener.
        mRsContext = new RsContext();
        mRsContext.setDevicesChangedCallback(new DeviceListener() {
            @Override
            public void onDeviceAttach() {
                configure_camera.setEnabled(true);
            }

            @Override
            public void onDeviceDetach() {
                configure_camera.setEnabled(false);
            }
        });

        // configuring camera
        configure_camera.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

            }
        });

    }


    // Checks if all permissions have been granted
    private void setupSpinners() {
        //Depth Resoltuion
        Spinner Depth_res = (Spinner) findViewById(R.id.Depth_res);
        ArrayAdapter<CharSequence> adapter = ArrayAdapter.createFromResource(this,
                R.array.depth_res, android.R.layout.simple_spinner_item);
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        Depth_res.setAdapter(adapter);
        //Depth FPS
        Spinner Depth_FPS = (Spinner) findViewById(R.id.Depth_FPS);
        ArrayAdapter<CharSequence> adapter1 = ArrayAdapter.createFromResource(this,
                R.array.FPS, android.R.layout.simple_spinner_item);
        adapter1.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        Depth_FPS.setAdapter(adapter1);

        //RGB Resoltuion
        Spinner RGB_res = (Spinner) findViewById(R.id.RGB_res);
        ArrayAdapter<CharSequence> adapter2 = ArrayAdapter.createFromResource(this,
                R.array.RGB_res, android.R.layout.simple_spinner_item);
        adapter2.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        RGB_res.setAdapter(adapter2);
        //RGB FPS
        Spinner RGB_FPS = (Spinner) findViewById(R.id.RGB_FPS);
        ArrayAdapter<CharSequence> adapter3 = ArrayAdapter.createFromResource(this,
                R.array.FPS, android.R.layout.simple_spinner_item);
        adapter3.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        RGB_FPS.setAdapter(adapter3);
=======
        // Set up intel camera
        Button intelSetup = (Button) findViewById(R.id.intel_setup);
        intelSetup.setClickable(false);
        final EditText intelRes = (EditText) findViewById(R.id.intel_resolution);
        EditText intelFPS = (EditText) findViewById(R.id.intel_FPS);

        intelSetup.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Toast.makeText(CameraActivity.this, "Camera Not Detected!", Toast.LENGTH_SHORT).show();
            }
        });
>>>>>>> 8f58b95ca63129ae98a1c65481e578685ce2585c
    }
}
