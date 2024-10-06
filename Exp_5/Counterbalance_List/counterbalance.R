set.seed(9999)

id <- seq(1:64)
counterbalance <- rep(0, times = 64)

cond_df <- as.data.frame(matrix(c(1, 2, 3, 4, 1, 2, 3, 4, 1, 1, 1, 1, 2, 2, 2, 2), ncol=2))
colnames(cond_df) <- c("Counterbalance", "FreqGroup")
cond_df

counterbalance_df <- as.data.frame(id)
counterbalance_df$FreqGroup <- c(1, 2)
counterbalance_df$Counterbalance <- c(1, 2, 3, 4)

counter <- 1
for (i in 1:(length(id) / 8)){
  
  rand_conds <- sample(c(1:8))
  
  for (r in rand_conds){
  counterbalance_df$FreqGroup[counter] <- cond_df[r, 2]
  counterbalance_df$Counterbalance[counter] <- cond_df[r, 1]
  counter <- counter + 1
  }
  
  
  
}

counterbalance_df

counterbalance_df$FreqGroup2 <- ifelse(counterbalance_df$FreqGroup == 1, "L", "H")
counterbalance_df$FreqGroup <- counterbalance_df$FreqGroup2

counterbalance_df <- counterbalance_df[,c(1, 2, 3)]

counterbalance_df

write.table(counterbalance_df, "counterbalance_list.csv", sep = ",",
            row.names = F)
