//
//  Review.swift
//  
//
//  Created by Akash Prasad on 5/1/25.
//

struct Review: Identifiable {
    let id: String
    let user: User
    let rating: Int
    let message: String
    let food: FoodItem
    let recommended: [FoodItem]
    let diningHall: DiningHall
}
