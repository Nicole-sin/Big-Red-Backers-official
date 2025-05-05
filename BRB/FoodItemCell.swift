//
//  FoodItemCell.swift
//  BRB
//
//  Created by Akash Prasad on 5/1/25.
//

import SwiftUI

struct FoodItemCell: View {
    
    let foodItem: FoodItem
    
    var body: some View {
        VStack {
            Image(foodItem.image)
                .frame(width: 300, height: 200)
                .cornerRadius(16)
            HStack {
                Text(foodItem.name)
                    .font(.system(size: 20, weight: .semibold))
                Text(foodItem.diningHall.name)
                    .font(.system(size: 14))
            }
        }
    }
}

#Preview {
    FoodItemCell(foodItem: FoodItem.dummyData[0])
}
