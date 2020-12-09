setwd("E:/MT/result")


lut<-read.table("lut.csv",header=TRUE)

# plot
scatter.smooth(x=lut$IntensityIn, y=lut$Luminance, main="Luminance ~ Intensity") 

# regression
lm_lut <- lm(Luminance ~ IntensityIn, data=lut)  # build linear regression model on full data
print(lm_lut)

# Luminance = 0.5885 + 514.724*IntensityIn
