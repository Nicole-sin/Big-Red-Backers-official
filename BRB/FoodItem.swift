//
//  FoodItem.swift
//  
//
//  Created by Akash Prasad on 5/1/25.
//

struct FoodItem {
    let id: String
    let name: String
    let image: String
    let diningHall: DiningHall
    
    static let dummyData = [
        FoodItem(id: "1", name: "Pepperoni Pizza", image: "pizza", diningHall: DiningHall(id: "1", name: "Morrison Dining", topItems: []))
    ]
}
