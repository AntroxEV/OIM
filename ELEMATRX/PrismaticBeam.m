function [Kst]=PrismaticBeam(E,I0,L)
% Dr Alessandro Tombari - https://github.com/AntroxEV
% Classic Euler-Bernoulli theory for prismatic beam
% 2 x 2 (2D Plane) Matrix - 2 DOFS displacement and rotation
% INPUT (singleton - scalar values):
% E: Elastic Modulus
% I0: cross-sectionalsecond moment of area
% L: beam length
% OUTPUT:
%Kst: 2x2 Stiffness Matrix


Kst =[ (12*E*I0)/L^3,  (6*E*I0)/L^2, -(12*E*I0)/L^3,  (6*E*I0)/L^2;
  (6*E*I0)/L^2,    (4*E*I0)/L,  -(6*E*I0)/L^2,    (2*E*I0)/L;
-(12*E*I0)/L^3, -(6*E*I0)/L^2,  (12*E*I0)/L^3, -(6*E*I0)/L^2;
  (6*E*I0)/L^2,    (2*E*I0)/L,  -(6*E*I0)/L^2,    (4*E*I0)/L];
