# practice
trial <- c(1:54, 1:54)
block <- c(rep(0, times = 108))
subblock <- c(rep(1, times = 54), rep(2, times = 54))
dependence <- c(rep(1, times = 54),  rep(-1, times = 54))
pertur_strength <- rep(1.325, times = 108)
reward_upper <- rep(0, times = 108)
reward_upper <- reward_upper + c(90, 80, 70, 60, 50, 40, 30, 20, 10)
reward_lower <- rep(0, times = 108)
reward_lower <- reward_lower + c(10, 20, 30, 40, 50, 60, 70, 80, 90)
pert_direct <- c(rep(0, times = 27), rep(1, times = 27), rep(0, times = 27), rep(1, times = 27))
training <- rep(1, times = 108)
preview <- c(rep("short", times = 9), rep("medium", times = 9), rep("long", times = 9),
             rep("short", times = 9), rep("medium", times = 9), rep("long", times = 9),
             rep("short", times = 9), rep("medium", times = 9), rep("long", times = 9),
             rep("short", times = 9), rep("medium", times = 9), rep("long", times = 9))


practice_conditions <- cbind(trial, block, subblock, dependence, pertur_strength, reward_upper, 
                             reward_lower, pert_direct, training, preview)

# experimental
trial <- c(1:54, 1:54, 1:54, 1:54, 1:54, 1:54)
block <- c(rep(1, times = 162), rep(2, times = 162))
subblock <- c(rep(1, times = 54), rep(2, times = 54), rep(3, times = 54), rep(1, times = 54),
              rep(2, times = 54), rep(3, times = 54))
dependence <- c(rep(1, times = 54),  rep(1, times = 54), rep(1, times = 54),  rep(-1, times = 54),
                rep(-1, times = 54),  rep(-1, times = 54))
pertur_strength <- rep(1.325, times = 324)
reward_upper <- rep(0, times = 324)
reward_upper <- reward_upper + c(90, 80, 70, 60, 50, 40, 30, 20, 10)
reward_lower <- rep(0, times = 324)
reward_lower <- reward_lower + c(10, 20, 30, 40, 50, 60, 70, 80, 90)
pert_direct <- c(rep(0, times = 27), rep(1, times = 27), rep(0, times = 27), rep(1, times = 27),
                 rep(0, times = 27), rep(1, times = 27), rep(0, times = 27), rep(1, times = 27),
                 rep(0, times = 27), rep(1, times = 27), rep(0, times = 27), rep(1, times = 27))
training <- rep(0, times = 324)
preview <- c(rep("short", times = 9), rep("medium", times = 9), rep("long", times = 9),
             rep("short", times = 9), rep("medium", times = 9), rep("long", times = 9),
             rep("short", times = 9), rep("medium", times = 9), rep("long", times = 9),
             rep("short", times = 9), rep("medium", times = 9), rep("long", times = 9),
             rep("short", times = 9), rep("medium", times = 9), rep("long", times = 9),
             rep("short", times = 9), rep("medium", times = 9), rep("long", times = 9),
             rep("short", times = 9), rep("medium", times = 9), rep("long", times = 9),
             rep("short", times = 9), rep("medium", times = 9), rep("long", times = 9),
             rep("short", times = 9), rep("medium", times = 9), rep("long", times = 9),
             rep("short", times = 9), rep("medium", times = 9), rep("long", times = 9),
             rep("short", times = 9), rep("medium", times = 9), rep("long", times = 9),
             rep("short", times = 9), rep("medium", times = 9), rep("long", times = 9))

experimental_conditions <- cbind(trial, block, subblock, dependence, pertur_strength, reward_upper, 
                          reward_lower, pert_direct, training, preview)

total_conditions <- rbind(practice_conditions, experimental_conditions)

total_conditions <- as.data.frame(total_conditions)

write.table(total_conditions, file = "Exp_Conditions.csv", sep = ";", fileEncoding = "UTF-8", row.names = F)