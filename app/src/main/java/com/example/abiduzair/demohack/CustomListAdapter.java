package com.example.abiduzair.demohack;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.TextView;

import java.util.ArrayList;
import java.util.Collection;

/**
 * Created by AbidUzair on 24-06-2017.
 */

public class CustomListAdapter extends ArrayAdapter<Product>{

    ArrayList<Product> productList;
    Context context;
    int resource;

    public CustomListAdapter(Context context,int resource,ArrayList<Product> productList){

        super(context,resource,productList);
        this.productList = productList;
        this.context = context;
        this.resource = resource;
    }

    @Override
    public int getCount() {
        return productList.size();
    }

    @NonNull
    @Override
    public View getView(int position, @Nullable View convertView, @NonNull ViewGroup parent) {

        ViewHolder viewHolder = new ViewHolder();
        if(convertView == null){
            LayoutInflater layoutInflater = (LayoutInflater) getContext().getSystemService(Activity.LAYOUT_INFLATER_SERVICE);
            convertView = layoutInflater.inflate(R.layout.listview_item,parent,false);
            viewHolder.imageView = (ImageView) convertView.findViewById(R.id.imageView);
            viewHolder.brandName = (TextView) convertView.findViewById(R.id.brandName);
            viewHolder.txtPrice = (TextView) convertView.findViewById(R.id.txtPrice);
            convertView.setTag(viewHolder);
        }
        else{
            viewHolder = (ViewHolder) convertView.getTag();
        }
        viewHolder.imageView.setImageResource( productList.get(position).getImage());
        viewHolder.brandName.setText(productList.get(position).getBrand());
        viewHolder.txtPrice.setText(String.valueOf(productList.get(position).getPrice()));
        return convertView;
    }

    static class ViewHolder {
        ImageView imageView;
        TextView brandName;
        TextView txtPrice;
    }
}