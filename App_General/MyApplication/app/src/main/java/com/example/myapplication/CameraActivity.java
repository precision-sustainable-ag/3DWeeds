package com.example.myapplication;
import android.os.Bundle;
import android.view.Window;

import androidx.appcompat.app.AppCompatActivity;

public class CameraActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        this.requestWindowFeature(Window.FEATURE_NO_TITLE);
        setContentView(R.layout.select_camera);

        // setting up all the spiners
        setupSpinners();

    }


    // Checks if all permissions have been granted
    private void setupSpinners() {
        //Depth Resoltuion
        /*
        Spinner Depth_res = (Spinner) findViewById(R.id.Depth_res);
        ArrayAdapter<CharSequence> adapter = ArrayAdapter.createFromResource(this, R.array, android.R.layout.simple_spinner_item);
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
         */
    }
}