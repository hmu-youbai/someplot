library(ggplot2)
library(tidyverse)



data <- read.csv("C:/Users/0.0/Desktop/2_hmc_csv/11.bed", header=F, sep="\t")


aaaa <- data %>% 
  mutate(element_bin = paste(V10, V11, sep=','))%>%    #bin1,bin2
  group_by(V9,V13,element_bin) %>%                     #chr,region
  
  #mutate(perc_mod_element= mean(V4))                  #level
  
  mutate(total_C_element_bin = sum(V5),total_T_element_bin = sum(V6))%>%          #nc,nt
  mutate(perc_mod_element= (total_C_element_bin / (total_C_element_bin + total_T_element_bin))*100)%>%
  
  
  group_by(V9,V13,element_bin) %>%                     #chr,region
  summarise(mean_mod_element=mean(perc_mod_element))%>%
  mutate(exp='BS')



bbbb <- data %>% 
  mutate(element_bin = paste(V10, V11, sep=','))%>% 
  group_by(V9,V13,element_bin) %>%
  
  mutate(perc_mod_element= mean(V4))%>%
  
  #mutate(total_C_element_bin = sum(V5),total_T_element_bin = sum(V6))%>%
  #mutate(perc_mod_element= (total_C_element_bin / (total_C_element_bin + total_T_element_bin))*100)%>%
  
  
  group_by(V9,V13,element_bin) %>%
  summarise(mean_mod_element=mean(perc_mod_element))%>%
  mutate(exp='BS')


bbbb$mean_mod_element=100*bbbb$mean_mod_element
a1=unique(aaaa$mean_mod_element)
b1=unique(100*bbbb$mean_mod_element)


p <- ggplot(bbbb,aes(x=V13,y=mean_mod_element)) +                       #region
  geom_boxplot(outlier.shape=NA, aes(color = exp)) +
  stat_summary(
    aes(color = exp),                                           
    geom = "point",
    fun.y = "mean",
    position = position_dodge(0.75),
    size = 2,
    shape = 1
  ) +
  stat_summary(aes(label=round(..y..,1), color = exp), fun.y=mean, 
               geom="text", size=2, position = position_dodge(0.75),
               vjust = -0.5) +
  theme_bw() + 
  theme(axis.text.x=element_text(angle=50,size=8,vjust=0.5)) + 
  theme(aspect.ratio=0.5)

p

