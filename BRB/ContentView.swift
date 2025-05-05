//
//  ContentView.swift
//  BRB
//
//  Created by Akash Prasad on 5/1/25.
//

import SwiftUI

struct ContentView: View {
    
    @State private var searchText = ""
    
    var body: some View {
        NavigationView {
            
            VStack {
                HStack {
                    Text("BRBs")
                        .font(.system(size: 16))
                    Image("Logo")
                        .imageScale(.large)
                        .foregroundStyle(.tint)
                }
                FoodItemCell(foodItem: FoodItem.dummyData[0])
            }
            .padding()
            
        }
        
    }
}

#Preview {
    ContentView()
}
