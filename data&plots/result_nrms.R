setwd(dirname(rstudioapi::getActiveDocumentContext()$path))


library(ggplot2)



dat_rms<-function(dat)
{
  datn <- paste(dat,".txt",sep="")
  
  # add names
  if (dat =="sub1") {
    nam <- 'GA'
  } else if ( dat =="sub2") {
    nam <- 'YX'
  } else if ( dat =="sub3") {
    nam <- 'MM'
  } else if ( dat =="sub4") {
    nam <- 'JP'
  } else {
    nam <- 'MW'
  }
  
  # read data
  dt.df<-read.table(datn,header=TRUE)
  nrms.df<-read.table("nrmsContrast.csv",sep=",",header=TRUE)
  
  # add new columns
  dt.df$nrms<-NA
  dt.df$matched_nrms<-NA
  
  # search the nrms contrast value according to tau, alpha, repeat
  for(i in 1:nrow(dt.df))
  {
    dt.df$nrms[i]<-nrms.df$nrmsConstrast[which(nrms.df$rep==dt.df$rep[i]
                                               &nrms.df$alpha==dt.df$a_test[i]
                                               &nrms.df$tau==dt.df$t_test[i])]
    dt.df$matched_nrms[i]<-nrms.df$nrmsConstrast[which(nrms.df$rep==dt.df$rep[i]
                                                       &nrms.df$alpha==dt.df$matched_alpha[i]
                                                       &nrms.df$tau==dt.df$t_test[i])] 
  }
  
  dt.df$matched_nrms_diff <- dt.df$matched_nrms - dt.df$nrms
  
  # factorization 
  dt.df$alpha<-as.factor(dt.df$a_test)
  dt.df$tau<-as.factor(dt.df$t_test)
  
  
  nrms_mean <- aggregate(matched_nrms_diff ~ alpha + tau, data = dt.df, FUN= "mean" )
  nrms_sd <- aggregate(matched_nrms_diff ~ alpha + tau, data = dt.df, FUN= "sd" )
  nrms_standard_nrms <- aggregate(nrms ~ alpha + tau, data = dt.df, FUN= "mean" )
  
  
  nrms.df <- cbind(nrms_mean,nrms_sd$matched_nrms_diff,nrms_standard_nrms$nrms)
  
  
  #rename column
  colnames(nrms.df)[4] <- "sd"
  colnames(nrms.df)[5] <- "standard_nrms"  
  #as.numeric(levels(f))[f]
  nrms.df$alpha<-as.numeric(levels(nrms.df$alpha))[nrms.df$alpha]
  nrms.df$nam<-as.factor(nam)
  
  return(nrms.df)
}  
  
dat0<- c()
for(i in 1:5)
{
  datn <- paste("sub",i,sep="")
  dat<-dat_rms(datn)
  dat0<-rbind(dat0,dat)
}




p<- ggplot(dat0, aes(x=standard_nrms, y=matched_nrms_diff, color=tau))+ 
  geom_point()+
  geom_line(aes(group=tau))+
  geom_errorbar(aes(ymin=matched_nrms_diff-1/2*sd, ymax=matched_nrms_diff+1/2*sd),width=0.02)+
  ylab("contrast difference")+
  xlab("standard nrms contrast")+
  #ylim(-5, 50)+
  xlim(0.02,0.4)+
  theme_classic()+
  facet_wrap(vars(nam), nrow=2)










'

tit="Matched and Standard normalized rms Contrast by Trial"
  
p<- ggplot(dat0, aes(x=rms, y=matched_rms, shape=alpha, color=tau)) + 
    geom_point() +
    geom_abline(slope=1,color="darkgrey") +
    #geom_vline(xintercept = 0, color="darkgrey")+
    xlab("standard rms contrast")+
    ylab("matched rms contrast")+
    xlim(0, 100)+
    ylim(0, 100)+
    #labs(title=tit)+
    theme(text = element_text(size=100))+
    theme_classic()+
    facet_wrap(vars(nam), nrow=2)

p
' 
