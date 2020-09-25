package com.example.myapplication;

import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.RecyclerView;

import android.Manifest;
import android.annotation.SuppressLint;
import android.app.ActivityManager;
import android.app.AlertDialog;
import android.app.Dialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.PeriodicSync;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.os.Build;
import android.os.Bundle;
import android.os.Environment;
import android.os.Looper;
import android.text.InputType;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.Window;
import android.widget.AdapterView;
import android.widget.BaseAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.gms.location.LocationCallback;
import com.google.android.gms.location.LocationRequest;
import com.google.android.gms.location.LocationResult;
import com.google.android.gms.location.LocationServices;
import com.google.android.material.floatingactionbutton.FloatingActionButton;

import java.io.File;
import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

public class FilesActivity extends AppCompatActivity {
    ListView filesList;
    List<String> fileNames = new ArrayList<String>();
    String rootPath;
    CustomAdapter customAdapter;
    boolean[] selected;
    File[] files;
    LinearLayout bottom_buttons;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        this.requestWindowFeature(Window.FEATURE_NO_TITLE);
        setContentView(R.layout.files);

        // display root path
        TextView file_path = findViewById(R.id.file_path);
        rootPath = getIntent().getStringExtra("ROOT");
        file_path.setText(rootPath.substring(rootPath.lastIndexOf('/')+1));

        // set up list views
        filesList = (ListView) findViewById(R.id.filesListView);
        customAdapter = new CustomAdapter(getApplicationContext(), fileNames);
        filesList.setAdapter(customAdapter);
        updateFilesList();
        customAdapter.notifyDataSetChanged();

        bottom_buttons = (LinearLayout) findViewById(R.id.bottom_buttons);

        // selecting an item
        // clicking on a directory
        filesList.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                // set selected
                selected[position] = !selected[position];
                boolean isOneSelected = false;
                for (boolean b : selected) {
                    if (b) {
                        isOneSelected = true;
                        break;
                    }
                }
                if (isOneSelected) {
                    bottom_buttons.setVisibility(View.VISIBLE);
                }
                else {
                    bottom_buttons.setVisibility(View.GONE);
                }
                customAdapter.notifyDataSetChanged();
            }
        });

        Button delete_button = findViewById(R.id.delete_file);
        Button preprocess_button = findViewById(R.id.preprocess_file);
        Button export_button = findViewById(R.id.export_file);

        // delete button click
        delete_button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                final AlertDialog.Builder deleteDialog = new AlertDialog.Builder(FilesActivity.this);
                deleteDialog.setTitle("Delete");
                deleteDialog.setMessage("Do you really want to delete these files?");
                deleteDialog.setPositiveButton("Yes", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        for (int i=0; i<files.length; i++) {
                            if (selected[i]) {
                                deleteFileOrFolder(files[i]);
                            }
                        }
                        Toast.makeText(FilesActivity.this, "File(s) deleted", Toast.LENGTH_SHORT).show();
                        updateFilesList();
                        customAdapter.notifyDataSetChanged();
                        bottom_buttons.setVisibility(View.GONE);
                    }
                });
                deleteDialog.setNegativeButton("Cancel", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        dialog.cancel();
                    }
                });
                deleteDialog.show();
            }
        });

        // Prepreocess button click
        preprocess_button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                final AlertDialog.Builder preDialog = new AlertDialog.Builder(FilesActivity.this);
                preDialog.setTitle("Preprocess");
                preDialog.setMessage("Do you really want to Preprocess these files?");
                preDialog.setPositiveButton("Yes", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        updateFilesList();
                        customAdapter.notifyDataSetChanged();
                        bottom_buttons.setVisibility(View.GONE);
                    }
                });
                preDialog.setNegativeButton("Cancel", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        dialog.cancel();
                    }
                });
                preDialog.show();
            }
        });

        // export button click
        export_button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                final AlertDialog.Builder exportDialog = new AlertDialog.Builder(FilesActivity.this);
                exportDialog.setTitle("Preprocess");
                exportDialog.setMessage("Do you really want to Export these files?");
                exportDialog.setPositiveButton("Yes", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        updateFilesList();
                        customAdapter.notifyDataSetChanged();
                        Toast.makeText(FilesActivity.this, "File(s) exported", Toast.LENGTH_SHORT).show();
                        bottom_buttons.setVisibility(View.GONE);
                    }
                });
                exportDialog.setNegativeButton("Cancel", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        dialog.cancel();
                    }
                });
                exportDialog.show();
            }
        });
    }

    public void updateFilesList() {
        File dir = new File(rootPath);
        files = dir.listFiles();
        int filesFoundCount;
        if (files != null) {
            filesFoundCount = files.length;
        } else {
            filesFoundCount = 0;
        }
        fileNames.clear();
        for (int i = 0; i < filesFoundCount; i++) {
            if (files[i].isFile()) {
                fileNames.add(files[i].getAbsolutePath());
            }
        }
        selected = new boolean[filesFoundCount];
    }

    public class CustomAdapter extends BaseAdapter {
        Context context;
        List<String> fileNames;
        LayoutInflater inflter;

        public CustomAdapter(Context applicationContext, List<String> fileNames) {
            this.context = context;
            this.fileNames = fileNames;
            inflter = (LayoutInflater.from(applicationContext));
        }

        @Override
        public int getCount() {
            return fileNames.size();
        }

        @Override
        public Object getItem(int i) {
            return fileNames.get(i);
        }

        @Override
        public long getItemId(int i) {
            return 0;
        }

        @Override
        public View getView(int i, View view, ViewGroup viewGroup) {
            view = inflter.inflate(R.layout.files_item, null);
            TextView file_name = (TextView) view.findViewById(R.id.file_name);
            file_name.setText(fileNames.get(i).substring(fileNames.get(i).lastIndexOf('/') + 1));
            if (selected!=null) {
                if (selected[i]) {
                    file_name.setBackgroundColor(Color.LTGRAY);
                } else {
                    file_name.setBackgroundColor(Color.WHITE);
                }
            }
            return view;
        }
    }

    private void deleteFileOrFolder(File fileOrDirectory) {
        if (fileOrDirectory.isDirectory()) {
            for (File child : fileOrDirectory.listFiles())
                deleteFileOrFolder(child);
        }

        fileOrDirectory.delete();
    }

    @Override
    protected void onRestart() {
        super.onRestart();
        finish();
        startActivity(getIntent());
    }

    @Override
    protected void onResume() {
        super.onResume();
        updateFilesList();
        customAdapter.notifyDataSetChanged();
    }
}