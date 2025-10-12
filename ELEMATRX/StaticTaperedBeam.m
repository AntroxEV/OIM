function [Kst]=StaticTaperedBeam(E,I0,alpha,L)
% Dr Alessandro Tombari - https://github.com/AntroxEV
% Static Stiffness Matrix of Tapered Euler Beam with I=I0(1+alpha*z)^3  
% 2 x 2 (2D Plane) Matrix - 2 DOFS displacement and rotation
% INPUT (singleton - scalar values):
% E: Elastic Modulus
% I: cross-sectional second moment of area
% alpha: slope of the second moment of area variation
% OUTPUT:
%Kst: 2x2 Stiffness Matrix

Kst =[-(E*I0*alpha^3*(alpha + 2))/(L^3*(2*alpha + 2*log(L) - 2*log(L*(alpha + 1)) + alpha*log(L) - alpha*log(L*(alpha + 1)))),                                                                                                                                              -(E*I0*alpha^3)/(L^2*(2*alpha + 2*log(L) - 2*log(L*(alpha + 1)) + alpha*log(L) - alpha*log(L*(alpha + 1)))),  (E*I0*alpha^3*(alpha + 2))/(L^3*(2*alpha + 2*log(L) - 2*log(L*(alpha + 1)) + alpha*log(L) - alpha*log(L*(alpha + 1)))),                                                                                           -(E*I0*alpha^3*(alpha + 1))/(L^2*(2*alpha + 2*log(L) - 2*log(L*(alpha + 1)) + alpha*log(L) - alpha*log(L*(alpha + 1))));
            -(E*I0*alpha^3)/(L^2*(2*alpha + 2*log(L) - 2*log(L*(alpha + 1)) + alpha*log(L) - alpha*log(L*(alpha + 1)))), (E*I0*(2*alpha + 2*log(L) - 2*log(L*(alpha + 1)) + 4*alpha*log(L) - 4*alpha*log(L*(alpha + 1)) + 3*alpha^2 + 2*alpha^2*log(L) - 2*alpha^2*log(L*(alpha + 1))))/(L*(2*alpha + 2*log(L) - 2*log(L*(alpha + 1)) + alpha*log(L) - alpha*log(L*(alpha + 1)))),              (E*I0*alpha^3)/(L^2*(2*alpha + 2*log(L) - 2*log(L*(alpha + 1)) + alpha*log(L) - alpha*log(L*(alpha + 1)))), -(E*I0*(alpha + 1)*(2*alpha + 2*log(L) - 2*log(L*(alpha + 1)) + 2*alpha*log(L) - 2*alpha*log(L*(alpha + 1)) + alpha^2))/(L*(2*alpha + 2*log(L) - 2*log(L*(alpha + 1)) + alpha*log(L) - alpha*log(L*(alpha + 1))));
 (E*I0*alpha^3*(alpha + 2))/(L^3*(2*alpha + 2*log(L) - 2*log(L*(alpha + 1)) + alpha*log(L) - alpha*log(L*(alpha + 1)))),                                                                                                                                               (E*I0*alpha^3)/(L^2*(2*alpha + 2*log(L) - 2*log(L*(alpha + 1)) + alpha*log(L) - alpha*log(L*(alpha + 1)))), -(E*I0*alpha^3*(alpha + 2))/(L^3*(2*alpha + 2*log(L) - 2*log(L*(alpha + 1)) + alpha*log(L) - alpha*log(L*(alpha + 1)))),                                                                                            (E*I0*alpha^3*(alpha + 1))/(L^2*(2*alpha + 2*log(L) - 2*log(L*(alpha + 1)) + alpha*log(L) - alpha*log(L*(alpha + 1))));
-(E*I0*alpha^3*(alpha + 1))/(L^2*(2*alpha + 2*log(L) - 2*log(L*(alpha + 1)) + alpha*log(L) - alpha*log(L*(alpha + 1)))),                                        -(E*I0*(alpha + 1)*(2*alpha + 2*log(L) - 2*log(L*(alpha + 1)) + 2*alpha*log(L) - 2*alpha*log(L*(alpha + 1)) + alpha^2))/(L*(2*alpha + 2*log(L) - 2*log(L*(alpha + 1)) + alpha*log(L) - alpha*log(L*(alpha + 1)))),  (E*I0*alpha^3*(alpha + 1))/(L^2*(2*alpha + 2*log(L) - 2*log(L*(alpha + 1)) + alpha*log(L) - alpha*log(L*(alpha + 1)))),                                              (E*I0*(alpha + 1)^2*(2*alpha + 2*log(L) - 2*log(L*(alpha + 1)) - alpha^2))/(L*(2*alpha + 2*log(L) - 2*log(L*(alpha + 1)) + alpha*log(L) - alpha*log(L*(alpha + 1))))];



 