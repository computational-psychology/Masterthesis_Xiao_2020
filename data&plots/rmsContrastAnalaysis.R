setwd(dirname(rstudioapi::getActiveDocumentContext()$path))


library(ggplot2)
library(gridExtra)



# function for plotting mean matched alpha by alpha and tau
plot_alpha_mean<-function(dat)
{
  datn <- paste(dat,".txt",sep="")
  
  # read data
  dm<-read.table(datn,header=TRUE)
  
  
  # set numeric variables into factors
  dm$a_test<-as.factor(dm$a_test)
  dm$t_test<-as.factor(dm$t_test)
  
  
  # aggregate mean and standard deviation of matched alpha by tau and alpha
  dm_mean <- aggregate(matched_alpha ~ a_test + t_test, data = dm, FUN= "mean" )
  dm_sd <- aggregate(matched_alpha ~ a_test + t_test, data = dm, FUN= "sd" )
  
  # create a new dataframe
  dm.df <- cbind(dm_mean,dm_sd$matched_alpha)
  
  
  # rename column
  colnames(dm.df)[1] <- "alpha"
  colnames(dm.df)[2] <- "tau"
  colnames(dm.df)[4] <- "sd"
  
  
  
  
  # plot
  p<- ggplot(dm.df, aes(x=alpha, y=matched_alpha, fill=tau)) + 
    geom_bar(stat="identity", color="black", 
             position=position_dodge()) +
    geom_errorbar(aes(ymin=matched_alpha-1/2*sd, ymax=matched_alpha+1/2*sd), width=.2,
                  position=position_dodge(.9)) +
    geom_segment(aes(x=0.5,xend=1.5,y=0.05,yend=0.05),linetype = "dashed")+
    geom_segment(aes(x=1.5,xend=2.5,y=0.1,yend=0.1),linetype = "dashed")+
    geom_segment(aes(x=2.5,xend=3.5,y=0.2,yend=0.2),linetype = "dashed")+
    geom_segment(aes(x=3.5,xend=4.5,y=0.4,yend=0.4),linetype = "dashed")+
    #scale_fill_grey(start = 0.2, end = 0.8)+
    ggtitle("Mean Matched Alpha by group",dat) 
  return(p)
}


# function for the rms contrast scatter plot of all 120 trials 
plot_rms<-function(dat)
{
  datn <- paste(dat,".txt",sep="")
  
  # read data
  dt.df<-read.table(datn,header=TRUE)
  rms.df<-read.table("rmsContrast.csv",sep=",",header=TRUE)
  
  # add new columns
  dt.df$rms<-NA
  dt.df$matched_rms<-NA
  
  # search the rms contrast value according to tau, alpha, repeat
  for(i in 1:nrow(dt.df))
  {
    dt.df$rms[i]<-rms.df$rmsConstrast[which(rms.df$rep==dt.df$rep[i]
                                            &rms.df$alpha==dt.df$a_test[i]
                                            &rms.df$tau==dt.df$t_test[i])]
    dt.df$matched_rms[i]<-rms.df$rmsConstrast[which(rms.df$rep==dt.df$rep[i]
                                                    &rms.df$alpha==dt.df$matched_alpha[i]
                                                    &rms.df$tau==dt.df$t_test[i])] 
  }
  
  
  dt.df$alpha<-as.factor(dt.df$a_test)
  dt.df$tau<-as.factor(dt.df$t_test)
  
  p<- ggplot(dt.df, aes(x=rms, y=matched_rms, shape=alpha, color=tau)) + 
    geom_point() +
    geom_abline(slope=1,color="darkgrey") +
    xlim(0, 90)+
    xlab("standard rms contrast")+
    ylab("matched rms contrast")+
    ylim(0, 90)+
    ggtitle("Rms Contrast",dat)
  return(p)
}


# function for plotting the mean rms contrast by alpha and tau

plot_rms_mean<-function(dat)
{
  datn <- paste(dat,".txt",sep="")
  
  # read data
  dt.df<-read.table(datn,header=TRUE)
  rms.df<-read.table("rmsContrast.csv",sep=",",header=TRUE)
  
  # add new columns
  dt.df$rms<-NA
  dt.df$matched_rms<-NA
  
  # search the rms contrast value according to tau, alpha, repeat
  for(i in 1:nrow(dt.df))
  {
    dt.df$rms[i]<-rms.df$rmsConstrast[which(rms.df$rep==dt.df$rep[i]
                                            &rms.df$alpha==dt.df$a_test[i]
                                            &rms.df$tau==dt.df$t_test[i])]
    dt.df$matched_rms[i]<-rms.df$rmsConstrast[which(rms.df$rep==dt.df$rep[i]
                                                    &rms.df$alpha==dt.df$matched_alpha[i]
                                                    &rms.df$tau==dt.df$t_test[i])] 
  }
  
  # factorization 
  dt.df$alpha<-as.factor(dt.df$a_test)
  dt.df$tau<-as.factor(dt.df$t_test)
  
  
  rms_mean <- aggregate(matched_rms ~ alpha + tau, data = dt.df, FUN= "mean" )
  rms_sd <- aggregate(matched_rms ~ alpha + tau, data = dt.df, FUN= "sd" )
  
  
  rms.df <- cbind(rms_mean,rms_sd$matched_rms)
  
  #rename column
  colnames(rms.df)[4] <- "sd"
  
  
  
  
  
  # plot
  p1<- ggplot(rms.df, aes(x=alpha, y=matched_rms, color=tau))+ 
    geom_point(position=position_dodge(.9))+
    geom_errorbar(aes(ymin=matched_rms-1/2*sd, ymax=matched_rms+1/2*sd),width=.2,position=position_dodge(.9))+
    ylab("matched rms contrast")+
    ggtitle("Mean Rms Contrast by Group",dat) 
  return(p1)
}


##########################################


dat1<-"sub5"
dat2<-"sub3"

p1<-plot_alpha_mean(dat1)
p2<-plot_alpha_mean(dat2)
p3<-plot_rms(dat1)
p4<-plot_rms(dat2)
p5<-plot_rms_mean(dat1)
p6<-plot_rms_mean(dat2)

grid.arrange(p1, p3, p5, p2, p4, p6, nrow = 2)