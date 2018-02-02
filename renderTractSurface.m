figure
outline = load_untouch_nii('FACT_176_comb.nii'); # Mask
color = load_untouch_nii('FACT_176.nii'); # Color mapping
smooth_outline = smooth3(outline.img);
smooth_color = smooth3(color.img);
iso = isosurface(smooth_outline,0.8,smooth_color);

colormap(jet);
colorbar;
caxis([0.2 0.6]);
hiso = patch(iso,'FaceColor','interp','EdgeColor','none');
lightangle(180,0);
hiso.FaceLighting='gouraud';
